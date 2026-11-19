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
     "key_cols", "biz_cols", "text_template", "member_trader_col"])
Endpoint.__new__.__defaults__ = (None, None)

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
}

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
    """生成诊断文本：有 text_template 用 {字段名} 渲染；否则取单一文本列。"""
    if ep.text_template:
        def _sub(m):
            v = raw.get(m.group(1))
            return "" if v is None else str(v)
        return re.sub(r"\{([A-Za-z0-9_]+)\}", _sub,
                      ep.text_template).strip()
    return (raw.get(ep.text_col) or "").strip()


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


def normalize_record(ep, raw):
    """把一条接口原始记录映射为诊断标准输入，返回 (record, fingerprint)。

    指纹与落库 build_fingerprint（scheduled）口径完全一致，便于跨轮次去重。
    """
    text = _render_text(ep, raw)
    ldate = _normalize_business_date(raw.get(ep.date_col))
    key = {c: raw.get(c) for c in ep.key_cols}
    key_json = json.dumps(key, ensure_ascii=False, sort_keys=True)
    params = {c: raw.get(c) for c in ep.biz_cols}
    # 需要会员反查的端点：补齐 member/client 供 runbook 取证。
    if ep.member_trader_col:
        member, client = _lookup_member(
            raw.get("exchCode"), raw.get(ep.member_trader_col))
        if member:
            params["member"] = member
        if client:
            params["client"] = client
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
                ep.path, page_no=page_no, page_size=page_size)
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
