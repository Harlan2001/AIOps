# -*- coding: utf-8 -*-
"""Dimple 实时监控采集器（接口级拉模式，准实时闭环）。

职责：
  - 端点注册表 ENDPOINTS：描述每个实时监控页面的接口路径与字段（先支持合规预警，
    后续新增页面只需追加一条注册）；
  - 字段映射 normalize_record：把接口记录转成诊断内核标准输入 dict；
  - 增量 + 幂等：游标状态文件记录最近处理指纹，已处理的直接跳过；落库层
    （trigger_type=scheduled 的 upsert）再兜底去重，保证不重不漏；
  - 采集主流程：分页拉取 → 映射 → 复用 DiagnosticService 诊断 → best-effort 落库。

诊断内核零改动；Dimple 接口异常按端点隔离，不影响其他端点与主服务。
"""
import json
import logging
import os
import re
import uuid
from collections import namedtuple
from datetime import datetime

from .. import paths
from ..config import load_config
from ..engine import db as eng_db
from ..service import DiagnosticService
from ..store import diag_repo
from .client import DimpleClient, DimpleError

_logger = logging.getLogger("ai_ops.dimple")

# 端点定义：id / 中文名 / 接口路径 / 文本列 / 日期列 / 时间列 / 主键列 / 业务列 /
# 文本模板（无单一文本列时用 {字段名} 拼描述，缺省 None 走 text_col）/
# 会员反查交易员字段（用 exchCode + 该字段反查 member/client，缺省 None 不反查）
Endpoint = namedtuple(
    "Endpoint",
    ["id", "label", "path", "text_col", "date_col", "time_col",
     "key_cols", "biz_cols", "text_template", "member_trader_col",
     "extra_body"])
Endpoint.__new__.__defaults__ = (None, None, None)

ENDPOINTS = {
    "dimple_compliance_alarm": Endpoint(
        "dimple_compliance_alarm", "合规预警",
        "/api/ksp-gp2-dimple/api/compliance-alarm-real-time-query/query",
        "alarmNote", "alarmDate", "alarmTime",
        ["alarmDate", "alarmTime", "memberId", "alarmType"],
        ["exchCode", "memberId", "alarmType"]),
    "dimple_self_deal": Endpoint(
        "dimple_self_deal", "自成交",
        "/api/ksp-gp2-dimple/api/self-deal-real-time-query/query",
        "", "matchTime", "matchTime",
        ["exchCode", "contractId", "matchNo", "matchTime"],
        ["exchCode", "contractId", "matchNo", "price", "qty",
         "buyTrader", "sellTrader"],
        "自成交预警：交易所 {exchCode}，合约 {contractId}，成交号 {matchNo}，"
        "成交时间 {matchTime}，买交易员 {buyTrader} 与卖交易员 {sellTrader} "
        "形成自成交，成交价 {price}，成交数量 {qty}",
        "buyTrader"),
    "dimple_violation_order": Endpoint(
        "dimple_violation_order", "违规委托",
        "/api/ksp-gp2-dimple/api/violation-order-real-time-query/query",
        "", "orderTime", "orderTime",
        ["exchCode", "localNo", "orderBatchNo", "orderNo", "orderTime"],
        ["exchCode", "contractId", "traderNo", "memberId", "clientId",
         "localNo", "bsFlag", "eoFlag", "qty", "price", "orderType", "status"],
        "违规委托：交易所 {exchCode}，合约 {contractId}，交易员 {traderNo}，"
        "本地委托号 {localNo}，买卖 {bsFlag} 开平 {eoFlag}，委托数量 {qty}，"
        "委托价格 {price}，定单类型 {orderType}，状态 {status}"),
    "dimple_trader_order": Endpoint(
        "dimple_trader_order", "交易员委托",
        "/api/ksp-gp2-dimple/api/trader-order-real-time-query/query",
        "", "orderTime", "orderTime",
        ["exchCode", "localNo", "orderBatchNo", "orderNo", "orderTime"],
        ["exchCode", "orderTime", "localNo", "orderBatchNo", "orderNo",
         "traderNo", "memberId", "clientId", "contractId", "qty", "price",
         "bsFlag", "eoFlag", "shFlag", "purposeCode", "matchQty",
         "orderType", "orderAttr", "status", "cancelTraderNo"],
        "交易员委托：交易所 {exchCode}，合约 {contractId}，交易员 {traderNo}，"
        "本地委托号 {localNo}，买卖 {bsFlag} 开平 {eoFlag}，委托数量 {qty}，"
        "委托价格 {price}，定单类型 {orderType}，状态 {status}"),
    "dimple_member_order": Endpoint(
        "dimple_member_order", "会员委托",
        "/api/ksp-gp2-dimple/api/member-order-real-time-query/query",
        "", "orderTime", "orderTime",
        ["exchCode", "memberId", "orderNo", "orderTime"],
        ["investId", "exchCode", "memberId", "clientId", "contractId",
         "bsFlag", "eoFlag", "shFlag", "orderType", "orderAttr", "status",
         "orderTime", "orderNo", "qty", "price", "matchQty", "traderNo"],
        "会员委托：交易所 {exchCode}，会员 {memberId}，合约 {contractId}，"
        "委托号 {orderNo}，买卖 {bsFlag} 开平 {eoFlag}，委托数量 {qty}，"
        "委托价格 {price}，定单类型 {orderType}，状态 {status}"),
    "dimple_quota_and_limit": Endpoint(
        "dimple_quota_and_limit", "额度与限额",
        "/api/ksp-gp2-dimple/api/quota-and-limit-real-time-query/query",
        "", "setDate", "setDate",
        ["exchCode", "memberId", "contractId", "configType"],
        ["exchCode", "memberId", "deliveryVarietyId", "contractId",
         "configType", "alarmValue", "limitValue", "setDate",
         "realValue", "ifOver"],
        "额度与限额：交易所 {exchCode}，会员 {memberId}，合约 {contractId}，"
        "配置类型 {configType}，预警值 {alarmValue}，限额值 {limitValue}，"
        "实际值 {realValue}，是否超限 {ifOver}"),
    "dimple_integrate_posi": Endpoint(
        "dimple_integrate_posi", "综合持仓",
        "/api/ksp-gp2-dimple/api/integrate-posi-real-time-query/query",
        "", "", "",
        ["contractId", "userId", "purposeCode", "memberId", "clientId", "varietyId"],
        ["contractId", "userId", "purposeCode", "memberId", "clientId",
         "varietyId", "qty", "costPrice", "lastPrice", "unrpl", "rpl",
         "allRpl", "profitloss"],
        "综合持仓：合约 {contractId}，用户 {userId}，用途 {purposeCode}，会员 "
        "{memberId}，客户 {clientId}，品种 {varietyId}，持仓量 {qty}，成本价 "
        "{costPrice}，最新价 {lastPrice}，浮动盈亏 {unrpl}，平仓盈亏 {rpl}，"
        "总盈亏 {allRpl}，盈亏 {profitloss}"),
    "dimple_estimate_account_remain": Endpoint(
        "dimple_estimate_account_remain", "预估账户资金",
        "/api/ksp-gp2-dimple/api/estimate-account-remain/query",
        "", "", "",
        ["exchCode", "memberId"],
        ["exchCode", "memberId", "lastRemain", "dayRemainAmt", "unretOutAmt",
         "unretInAmt", "cashBalance", "expectRemainAtm", "note"],
        "预估账户资金：交易所 {exchCode}，会员 {memberId}，上日结余 {lastRemain}，"
        "当日发生额 {dayRemainAmt}，未划出 {unretOutAmt}，未划入 {unretInAmt}，"
        "现金余额 {cashBalance}，预计结余 {expectRemainAtm}，备注 {note}"),
    "dimple_estimate_storage_remain": Endpoint(
        "dimple_estimate_storage_remain", "预估库存",
        "/api/ksp-gp2-dimple/api/estimate-storage-remain/query",
        "", "", "",
        ["exchCode", "memberId", "clientId", "deliveryVarietyId"],
        ["exchCode", "memberId", "clientId", "deliveryVarietyId", "lastRemain",
         "dayRemainQty", "unretOutQty", "unretInQty", "realtimeStorage",
         "expectRemainQty", "note"],
        "预估库存：交易所 {exchCode}，会员 {memberId}，客户 {clientId}，交割品种 "
        "{deliveryVarietyId}，上日结余 {lastRemain}，当日发生量 {dayRemainQty}，"
        "未划出 {unretOutQty}，未划入 {unretInQty}，实时库存 {realtimeStorage}，"
        "预计结余 {expectRemainQty}，备注 {note}"),
    "dimple_fund_realtime": Endpoint(
        "dimple_fund_realtime", "资金实时",
        "/api/ksp-gp2-dimple/api/fund-realtime-query/query",
        "", "", "",
        ["exchCode", "memberId"],
        ["exchCode", "memberId", "exchName", "lastRemain", "lastMargin",
         "moneyIn", "moneyOut", "buyAmount", "sellAmount", "offsetProfit",
         "tradeMargin", "frozenMargin", "avail", "availFloat", "frozenPremium",
         "buySellPremium", "lawLastForzenAmt", "lawForzenAmt"],
        "资金实时：交易所 {exchCode}，会员 {memberId}，上日结余 {lastRemain}，"
        "上日保证金 {lastMargin}，入金 {moneyIn}，出金 {moneyOut}，买入额 "
        "{buyAmount}，卖出额 {sellAmount}，平仓盈亏 {offsetProfit}，交易保证金 "
        "{tradeMargin}，冻结保证金 {frozenMargin}，可用资金 {avail}"),
    "dimple_member_inventory": Endpoint(
        "dimple_member_inventory", "会员库存",
        "/api/ksp-gp2-dimple/api/member-inventory-real-query/query",
        "", "", "",
        ["deliveryVarietyId", "memberId", "clientId"],
        ["deliveryVarietyId", "memberId", "clientId", "totalStorage",
         "availableStorage", "frozenStorage", "pendStorage", "mortStorage",
         "lawFrozenStorage", "transferFrozenStorage", "setoffFrozenStorage",
         "realUnqty", "custTotalStorage"],
        "会员库存：交割品种 {deliveryVarietyId}，会员 {memberId}，客户 {clientId}，"
        "总库存 {totalStorage}，可用 {availableStorage}，冻结 {frozenStorage}，"
        "待处理 {pendStorage}，质押 {mortStorage}，实际库存 {realUnqty}"),
    "dimple_real_time_arbi_quot": Endpoint(
        "dimple_real_time_arbi_quot", "实时套利行情",
        "/api/ksp-gp2-dimple/api/real-time-arbi-quot/query",
        "", "", "",
        ["contractId"],
        ["contractId", "openPrice", "highPrice", "lowPrice", "lastPrice",
         "change1", "change2", "bidPrice", "bidQty", "askPrice", "askQty",
         "closePrice", "clearPrice", "lastClear", "riseLimit", "fallLimit",
         "lastClose"],
        "实时套利行情：合约 {contractId}，开盘价 {openPrice}，最高 {highPrice}，"
        "最低 {lowPrice}，最新价 {lastPrice}，买价 {bidPrice}，买量 {bidQty}，"
        "卖价 {askPrice}，卖量 {askQty}，收盘价 {closePrice}，结算价 {clearPrice}"),
    "dimple_real_time_quot": Endpoint(
        "dimple_real_time_quot", "实时行情",
        "/api/ksp-gp2-dimple/api/real-time-quot/query",
        "", "", "",
        ["contractId"],
        ["contractId", "openPrice", "highPrice", "lowPrice", "lastPrice",
         "change1", "change2", "bidPrice", "bidQty", "askPrice", "askQty",
         "matchTotQty", "openInterest", "change", "closePrice", "clearPrice",
         "lastClear", "riseLimit", "fallLimit", "lastClose"],
        "实时行情：合约 {contractId}，开盘价 {openPrice}，最高 {highPrice}，最低 "
        "{lowPrice}，最新价 {lastPrice}，买价 {bidPrice}，买量 {bidQty}，卖价 "
        "{askPrice}，卖量 {askQty}，成交量 {matchTotQty}，持仓量 {openInterest}，"
        "收盘价 {closePrice}，结算价 {clearPrice}"),
    "dimple_self_run_trader_stock": Endpoint(
        "dimple_self_run_trader_stock", "自营交易员库存",
        "/api/ksp-gp2-dimple/api/self-run-trader-stock-real-query/query",
        "", "", "",
        ["memberId", "clientId", "deliveryVarietyId", "traderNo", "purposeCode"],
        ["memberId", "clientId", "deliveryVarietyId", "traderNo", "purposeCode",
         "totalStorage", "availableStorage", "frozenStorage", "pendStorage",
         "mortStorage", "lawFrozenStorage", "transferFrozenStorage",
         "setoffFrozenStorage"],
        "自营交易员库存：会员 {memberId}，客户 {clientId}，交割品种 "
        "{deliveryVarietyId}，交易员 {traderNo}，用途 {purposeCode}，总库存 "
        "{totalStorage}，可用 {availableStorage}，冻结 {frozenStorage}，待处理 "
        "{pendStorage}，质押 {mortStorage}"),
}

# 字段在当前无数据时无法预知的端点：统一用通用渲染（有数据时自动拼接全部字段）。
# 元组：(id 后缀, 中文名, 接口路径, extra_body)
_GENERIC = [
    ("alarm_note", "预警说明",
     "/api/ksp-gp2-dimple/api/alarm-note-real-time-query/query",
     {"isMember": True}),
    ("client_storage_flow", "客户库存流水",
     "/api/ksp-gp2-dimple/api/client-storage-flow-real-time-query/query", None),
    ("defer_fee_rate", "递延费率",
     "/api/ksp-gp2-dimple/api/defer-fee-rate-real-time-query/query", None),
    ("member_exposure", "会员风险敞口",
     "/api/ksp-gp2-dimple/api/member-exposure-real-time-query/query", None),
    ("rfq_default_declaration", "保证金询价违约申报",
     "/api/ksp-gp2-dimple/api/rfq-default-declaration-real-time-query/query", None),
    ("rfq_match", "询价成交",
     "/api/ksp-gp2-dimple/api/rfq-match-real-time-query/query", None),
    ("rfq_uncheck_match", "询价未确认成交",
     "/api/ksp-gp2-dimple/api/rfq-uncheck-match-real-time-query/query", None),
    ("trade_purpose_posi", "交易用途持仓",
     "/api/ksp-gp2-dimple/api/trade-purpose-posi-real-time-query/query", None),
    ("trader_credit_limit", "交易员授信额度",
     "/api/ksp-gp2-dimple/api/trader-credit-limit-real-time-query/query", None),
    ("trader_delivery_declare_trade", "交易员交割申报成交",
     "/api/ksp-gp2-dimple/api/trader-delivery-declare-trade-real-time-query/query", None),
    ("trader_exposure", "交易员风险敞口",
     "/api/ksp-gp2-dimple/api/trader-exposure-real-time-query/query", None),
    ("member_hold", "会员持仓",
     "/api/ksp-gp2-dimple/api/member-hold-real-query/query", None),
    ("member_qty_weight_limit", "会员数量重量限额",
     "/api/ksp-gp2-dimple/api/member-qty-weight-limit-time-query/query", None),
    ("member_transaction", "会员交易",
     "/api/ksp-gp2-dimple/api/member-transaction-real-query/query", None),
    ("member_wrong_order", "会员错单",
     "/api/ksp-gp2-dimple/api/member-wrong-single-real-query/query", None),
    ("self_run_trader_deal", "自营交易员成交",
     "/api/ksp-gp2-dimple/api/self-run-trader-deal-real-query/query", None),
    ("self_run_trader_hold", "自营交易员持仓",
     "/api/ksp-gp2-dimple/api/self-run-trader-hold-real-query/query", None),
    ("self_run_trader_wrong", "自营交易员错单",
     "/api/ksp-gp2-dimple/api/self-run-trader-wrong-sin-real-query/query", None),
    ("trader_qty_weight_limit", "交易员数量重量限额",
     "/api/ksp-gp2-dimple/api/trader-qty-weight-limit-time-query/query", None),
    ("option_exec", "期权行权",
     "/api/ksp-gp2-dimple/api/option-exec-real-time-query/query-trader", None),
    ("self_hedging", "自营套保",
     "/api/ksp-gp2-dimple/api/self-hedging-real-time-query/query-trader", None),
    ("rfq_posi", "询价持仓",
     "/api/ksp-gp2-dimple/api/rfq-posi-real-time-query/query-trader",
     {"dueDateStart": "2026-01-01", "dueDateEnd": "2026-12-31"}),
    ("trader_delivery_declare", "交易员交割申报",
     "/api/ksp-gp2-dimple/api/trader-delivery-declare-real-time-query/query-delivery",
     None),
]
for _suf, _label, _path, _body in _GENERIC:
    _eid = "dimple_" + _suf
    ENDPOINTS[_eid] = Endpoint(
        _eid, _label, _path, "", "", "", [], [], None, None, _body)

# ---------------------------------------------------------------------------
# 异常过滤：实时监控只保留"确实是异常/告警"的记录，正常业务数据不诊断、不落库。
#
# 分两类：
#   1) BUSINESS_ENDPOINTS —— 纯业务数据查询页（行情/持仓/资金/库存/委托/成交/
#      申报/流水等），整页都是正常数据，直接跳过；
#   2) ANOMALY_PREDICATES —— 监控页里需要按字段判断是否异常的端点，
#      判定函数返回 True 才是异常（如额度限额只有 ifOver 表示超限才告警）。
# 其余端点（合规预警、自成交、违规委托、错单、敞口等）默认即告警，记录保留。
# ---------------------------------------------------------------------------
BUSINESS_ENDPOINTS = {
    # 正常委托/成交流水
    "dimple_trader_order", "dimple_member_order",
    # 行情类
    "dimple_real_time_quot", "dimple_real_time_arbi_quot",
    # 持仓类
    "dimple_integrate_posi", "dimple_trade_purpose_posi",
    "dimple_member_hold", "dimple_self_run_trader_hold",
    "dimple_rfq_posi",
    # 资金类
    "dimple_fund_realtime", "dimple_estimate_account_remain",
    # 库存类
    "dimple_member_inventory", "dimple_self_run_trader_stock",
    "dimple_estimate_storage_remain", "dimple_client_storage_flow",
    # 成交类
    "dimple_self_run_trader_deal", "dimple_member_transaction",
    "dimple_rfq_match", "dimple_rfq_uncheck_match",
    # 配置/费率/限额查询（无超限标志，仅展示当前参数）
    "dimple_defer_fee_rate", "dimple_member_qty_weight_limit",
    "dimple_trader_qty_weight_limit",
    # 业务操作/申报记录
    "dimple_option_exec", "dimple_self_hedging",
    "dimple_trader_delivery_declare",
    "dimple_trader_delivery_declare_trade",
    "dimple_rfq_default_declaration",
}

# 表示"超限/成立"的取值与历史查询共用，避免双层过滤口径漂移。
_TRUE_TOKENS = diag_repo.QUOTA_OVER_TOKENS


def _quota_is_over(raw):
    """额度与限额：仅当 ifOver 表示超限时才是异常，兼容 JSON 布尔和数值。"""
    value = raw.get("ifOver")
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value == 1
    return str(value or "").strip().lower() in _TRUE_TOKENS


ANOMALY_PREDICATES = {
    "dimple_quota_and_limit": _quota_is_over,
}


def is_anomaly(ep_id, raw):
    """判断一条实时记录是否为真实异常。业务数据页返回 False；
    有记录级判定规则的按规则判定；其余告警类端点默认 True。"""
    if ep_id in BUSINESS_ENDPOINTS:
        return False
    pred = ANOMALY_PREDICATES.get(ep_id)
    if pred is not None:
        return bool(pred(raw))
    return True

_DEFAULTS = {
    "enabled": False,
    "base_url": "",
    "username": "",
    "password": "",
    "client_id": "testjwtclientid",
    "client_secret": "XY7kmzoNzl100",
    "timeout": 10,
    "interval_minutes": 5,
    "page_size": 50,
    "max_pages": 5,          # 每次采集每个端点的硬上限页数，防止无限拉取
    "endpoints": [],         # 留空 = 全部已注册端点
    "recent_keep": 1000,      # 游标内存留的最近指纹条数
}


def load_dimple_config():
    """读取 dimple 配置并补默认值。"""
    out = dict(_DEFAULTS)
    out.update(load_config("dimple"))
    return out


def is_enabled():
    """实时监控总开关，缺省关闭。"""
    return bool(load_dimple_config().get("enabled", False))


def _render_text(ep, raw):
    """生成诊断文本：有 text_template 用 {字段名} 渲染；否则取单一文本列；
    两者都没有（无数据时无法预知字段的端点）时，自动拼接全部非空字段。"""
    if ep.text_template:
        def _sub(m):
            v = raw.get(m.group(1))
            return "" if v is None else str(v)
        return re.sub(r"\{([A-Za-z0-9_]+)\}", _sub,
                      ep.text_template).strip()
    if ep.text_col:
        return (raw.get(ep.text_col) or "").strip()
    # 通用兜底：把整条记录的非空字段拼成可读文本。
    parts = ["%s：%s" % (k, v) for k, v in raw.items()
             if v not in (None, "")]
    return ("%s：" % ep.label + "，".join(parts)).strip()


def _normalize_business_date(value):
    """归一化为 8 位业务日期 YYYYMMDD（日志表 business_date 为 varchar(8)）。

    兼容 "20261118"、"2026-11-18 10:20:31"、"2026/11/18"；实时接口的时间列
    可能只有 "HH:MM:SS"（数据均为当天），这类归到采集当天；空值同样归当天。
    """
    today = datetime.now().strftime("%Y%m%d")
    s = str(value or "").strip()
    if not s:
        return today
    m = re.match(r"(\d{4})[-/]?(\d{1,2})[-/]?(\d{1,2})", s)
    if m:
        y, mo, d = m.groups()
        return "%s%02d%02d" % (y, int(mo), int(d))
    digits = re.sub(r"\D", "", s)
    if len(digits) == 8:
        return digits
    # 只有时间（HH:MM:SS）等无法取到日期的情况，实时数据归到采集当天。
    return today


def _lookup_member(exch_code, trader_no):
    """用交易所+交易员反查 (member_id, client_id)；失败/无记录返回 (None, None)。

    实时接口本身不含会员/客户，经 vw_member_trader_operator 关系视图补齐，
    供 runbook 的单表取证 SQL 使用。反查失败不阻断主诊断。
    """
    if not exch_code or not trader_no:
        return None, None
    sql = ("SELECT member_id, client_id FROM dimple.vw_member_trader_operator "
           "WHERE trader_no = :t AND exch_code = :e LIMIT 1")
    try:
        cols, rows = eng_db.query(sql, {"t": trader_no, "e": exch_code})
    except Exception as e:  # noqa: BLE001 - 反查仅为增强，不阻断
        _logger.warning("会员反查失败（不阻断诊断）：%s", e)
        return None, None
    if not rows:
        return None, None
    d = dict(zip(cols, rows[0]))
    return d.get("member_id"), d.get("client_id")


# Dimple 接口原始英文字段（驼峰） -> 诊断 runbook 标准绑定参数名。
# 错单等通用端点的原始字段是英文名，而 runbook 里多为简写参数（如 :contract），
# 在适配层统一归一，避免主证据因缺参而无法查库、置信度被误降。
FIELD_ALIASES = {
    "contractId": ("contract",),
    "memberId": ("member",),
    "clientId": ("client",),
    "traderNo": ("trader",),
    "varietyId": ("variety",),
    "exchCode": ("exch",),
    "marketType": ("market",),
    "purposeCode": ("purpose",),
    "price": ("order_price",),
}


def _apply_field_aliases(params, raw):
    """把原始英文字段的值补写到 runbook 期望的标准参数名。

    仅在目标键缺失或为空时补写，不覆盖已有的会员反查结果；原始字段保留在
    params 中（如 :contractId 仍可被对应 runbook 使用）。"""
    for src, targets in FIELD_ALIASES.items():
        val = raw.get(src)
        if val in (None, ""):
            continue
        for tgt in targets:
            if params.get(tgt) in (None, ""):
                params[tgt] = val
    return params


def normalize_record(ep, raw):
    """把一条接口原始记录映射为诊断标准输入，返回 (record, fingerprint)。

    指纹与落库 build_fingerprint（scheduled）口径完全一致，便于跨轮次去重。
    """
    text = _render_text(ep, raw)
    ldate = _normalize_business_date(raw.get(ep.date_col))
    key = {c: raw.get(c) for c in ep.key_cols}
    key_json = json.dumps(key, ensure_ascii=False, sort_keys=True)
    # biz_cols 留空（字段未知的端点）时，自动带上全部原始字段。
    if ep.biz_cols:
        params = {c: raw.get(c) for c in ep.biz_cols}
    else:
        params = dict(raw)
    # 需要会员反查的端点：补齐 member/client 供 runbook 取证。
    if ep.member_trader_col:
        member, client = _lookup_member(
            raw.get("exchCode"), raw.get(ep.member_trader_col))
        if member:
            params["member"] = member
        if client:
            params["client"] = client
    # 英文字段归一到 runbook 标准参数（contractId -> contract 等），不覆盖已有值。
    _apply_field_aliases(params, raw)
    record = {
        "text": text,
        "ldate": ldate,
        "errcode": 0,
        "lsection": "",
        "source": ep.id,
        "source_label": ep.label,
        "key": key,
        "params": params,
    }
    fingerprint = diag_repo.build_fingerprint(
        "scheduled", ep.id, ldate, text, key_json)
    return record, fingerprint


class CursorStore:
    """游标状态持久化（var/state/dimple_cursor.json），原子写、重启不丢。"""

    def __init__(self, path=None):
        self.path = path or paths.state_file("dimple_cursor")
        self.data = self._load()

    def _load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except FileNotFoundError:
            return {}

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = str(self.path) + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.path)

    def _ep_state(self, ep_id):
        return self.data.setdefault("endpoints", {}).setdefault(ep_id, {})

    def seen(self, ep_id, fingerprint):
        recent = self._ep_state(ep_id).get("recent") or []
        return fingerprint in recent

    def mark(self, ep_id, fingerprint, last_key):
        state = self._ep_state(ep_id)
        recent = state.setdefault("recent", [])
        recent.append(fingerprint)
        keep = int(load_dimple_config().get("recent_keep", 1000))
        if len(recent) > keep:
            del recent[:len(recent) - keep]
        state["last_key"] = last_key
        state["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def build_client(cfg):
    return DimpleClient(
        base_url=cfg["base_url"],
        username=cfg["username"],
        password=cfg["password"],
        client_id=cfg.get("client_id") or "testjwtclientid",
        client_secret=cfg.get("client_secret") or "XY7kmzoNzl100",
        timeout=cfg.get("timeout", 10))


def _is_summary_row(raw):
    """识别接口返回的"合计/小计"汇总行（非真实告警，不应落库）。

    汇总行特征：某个字段值含"合计/小计"（界面文案可能带空格，如"合 计"），
    且主键业务字段多为空。这里去空格后通用判断，不依赖具体字段名。
    """
    return any(
        isinstance(v, str) and (
            "合计" in re.sub(r"\s", "", v) or "小计" in re.sub(r"\s", "", v))
        for v in raw.values())


def _fetch_endpoint(client, ep, cfg, cursor):
    """分页拉取单个端点，返回待诊断的 [(record, fingerprint, last_key), ...]。"""
    page_size = int(cfg.get("page_size", 50))
    max_pages = int(cfg.get("max_pages", 5))
    pending, last_key, fetch_errors = [], None, 0
    page_no = 1

    while page_no <= max_pages:
        try:
            data = client.query_page(
                ep.path, page_no=page_no, page_size=page_size,
                filters=ep.extra_body)
        except DimpleError as e:
            _logger.warning("端点 %s 第 %d 页拉取失败（已中止该端点）：%s",
                            ep.id, page_no, e)
            fetch_errors += 1
            break

        rows = data.get("records") or []
        if not rows:
            break
        for raw in rows:
            # 跳过合计/小计汇总行，只处理真实告警。
            if _is_summary_row(raw):
                continue
            # 异常过滤：正常业务数据（行情/持仓/资金/库存等）不诊断、不落库。
            if not is_anomaly(ep.id, raw):
                continue
            last_key = {c: raw.get(c) for c in ep.key_cols}
            record, fingerprint = normalize_record(ep, raw)
            # 文本为空无法诊断；游标已记录的直接跳过，避免重复诊断。
            if not record["text"] or cursor.seen(ep.id, fingerprint):
                continue
            pending.append((record, fingerprint, last_key))

        total_pages = int(data.get("pages", 0) or 0)
        if total_pages and page_no >= total_pages:
            break
        if len(rows) < page_size:
            break
        page_no += 1

    return pending, last_key, fetch_errors


def run_realtime_collection(svc=None):
    """执行一次实时采集，返回摘要；未启用时返回 disabled。

    复用 DiagnosticService 诊断，trigger_type=scheduled，落库自动 upsert 去重。
    """
    cfg = load_dimple_config()
    if not cfg.get("enabled", False):
        return {"status": "disabled"}

    ep_ids = cfg.get("endpoints") or list(ENDPOINTS)
    client = build_client(cfg)
    cursor = CursorStore()
    batch_id = uuid.uuid4().hex
    service = svc or DiagnosticService()

    summary = {"status": "ok", "batch_id": batch_id,
               "fetched": 0, "new": 0, "errors": 0, "endpoints": {}}

    for ep_id in ep_ids:
        ep = ENDPOINTS.get(ep_id)
        if ep is None:
            summary["endpoints"][ep_id] = {"error": "未知端点"}
            continue

        pending, last_key, fetch_errors = _fetch_endpoint(
            client, ep, cfg, cursor)

        recs = [item[0] for item in pending]
        diag_errors = 0
        if recs:
            pairs = service.diagnose_many_isolated(
                recs, _ctx={"trigger_type": "scheduled",
                            "batch_id": batch_id})
            for (record, result), (_rec, fp, lk) in zip(pairs, pending):
                if isinstance(result, dict) and result.get("_diagnose_error"):
                    diag_errors += 1
                # 诊断完成后再标记游标，异常条目也标记，避免下轮反复重试同一条。
                cursor.mark(ep_id, fp, lk)

        summary["endpoints"][ep_id] = {
            "fetched": len(recs), "new": len(recs),
            "fetch_errors": fetch_errors, "errors": diag_errors,
            "last_key": last_key}
        summary["fetched"] += len(recs)
        summary["new"] += len(recs)
        summary["errors"] += diag_errors

    cursor.save()
    _logger.info("实时采集完成 batch=%s 新增=%d 诊断异常=%d",
                 batch_id, summary["new"], summary["errors"])
    return summary
