# -*- coding: utf-8 -*-
"""错误历史记录取数（GaussDB 版，替代 Oracle 的 engine/tlog.py）。

信创环境无全量日志（ULOG.TLOG 不存在），诊断输入来自 GaussDB 中按错误域
拆分的错误/报警历史表。本模块：
  - 用 SOURCES 注册表描述每个错误来源（当日表/历史表、日期列、文本列、主键、业务列）
  - get_record / list_records / list_by_date 取数
  - 统一标准化为诊断记录 dict（对齐 pipeline / rule_engine）

诊断记录字段：
  text       : 报错文本（来源表的错误原因/报警信息列）
  ldate      : 业务日期（YYYYMMDD）
  errcode    : 错误码（错误表无独立错误码，默认 0，类型靠文本匹配）
  lsection   : 调用链位置（错误表无，留空）
  source     : 错误来源标识；source_label 为中文名
  key        : 主键 dict（记录追溯）
  params     : runbook 参数（业务字段原列名 + 短名 member/client/contract...）
"""
from collections import namedtuple

from .db import query

SCHEMA = "dimple"

Source = namedtuple(
    "Source",
    ["id", "label", "his", "today", "date_col", "text_col", "key_cols", "biz_cols"])

# 业务字段原列名 -> runbook 习惯短名
_SHORT = {
    "member_id": "member", "client_id": "client", "contract_id": "contract",
    "trader_no": "trader", "exch_code": "exch", "bs_flag": "bs",
    "eo_flag": "eo", "user_id": "user", "variety_id": "variety",
    "market_type": "market", "purpose_code": "purpose",
}

SOURCES = {
    "ftr_err": Source(
        "ftr_err", "期货错误委托",
        "tt_his_ftr_err_order", "tt_ftr_err_order",
        "trade_date", "reason",
        ["trade_date", "trader_no", "local_no", "purpose_code"],
        ["member_id", "client_id", "contract_id", "exch_code", "trader_no",
         "bs_flag", "eo_flag", "qty", "order_type", "status",
         "force_offset_reason", "purpose_code"]),
    "quote_err": Source(
        "quote_err", "报价错误委托",
        "tt_his_quote_err_order", "tt_quote_err_order",
        "trade_date", "reason",
        ["trade_date", "trader_no", "local_no"],
        ["member_id", "client_id", "contract_id", "trader_no",
         "bs_flag", "order_type", "status"]),
    "alarm": Source(
        "alarm", "敞口/止损报警",
        "tc_his_alarm_note", "tc_alarm_note",
        "alarm_date", "alarm_note",
        ["alarm_date", "seq_no", "alarm_type"],
        ["member_id", "client_id", "user_id", "variety_id",
         "market_type", "purpose_code", "alarm_type"]),
    "quote_alarm": Source(
        "quote_alarm", "报价风控预警",
        "tc_his_quote_alarm_note", "tc_quote_alarm_note",
        "trade_date", "risk_info",
        ["trade_date", "seq_no"],
        ["member_id", "contract_id", "risk_type"]),
    "rule_alarm": Source(
        "rule_alarm", "合规报警",
        "tc_his_rule_alarm_note", "tc_rule_alarm_note",
        "alarm_date", "alarm_note",
        ["alarm_date", "seq_no", "member_id", "alarm_type"],
        ["client_id", "exch_code", "member_id", "alarm_type"]),
    "data_check": Source(
        "data_check", "数据检查",
        "tp_data_check_log", None,
        "check_date", "err_desc",
        ["check_date", "seq_no"],
        ["check_item", "op_flag", "operator", "exch_code"]),
    "flow_control": Source(
        "flow_control", "结算流程控制",
        "tc_his_flow_control", None,
        "clear_date", "err_msg",
        ["clear_date", "flow_code", "exch_code"],
        ["flow_code", "exch_code", "oper_name", "oper_result"]),
}


def _table(src, history):
    name = src.his if history else (src.today or src.his)
    return "%s.%s" % (SCHEMA, name)


def _select(src, columns, history, where=None, params=None, limit=None):
    sql = "SELECT %s FROM %s" % (", ".join(columns), _table(src, history))
    if where:
        sql += " WHERE " + where
    if limit:
        sql += " LIMIT %d" % int(limit)
    cols, rows = query(sql, params)
    return [dict(zip(cols, r)) for r in rows]


def _all_cols(src):
    return sorted(set([src.date_col, src.text_col] + src.key_cols + src.biz_cols))


def _normalize(src, d):
    params = {}
    for col in src.biz_cols:
        val = d.get(col)
        params[col] = val
        short = _SHORT.get(col)
        if short:
            params[short] = val
    return {
        "text": (d.get(src.text_col) or "").strip(),
        "ldate": d.get(src.date_col) or "",
        "errcode": 0,
        "lsection": "",
        "source": src.id,
        "source_label": src.label,
        "key": {k: d.get(k) for k in src.key_cols},
        "params": params,
    }


def get_record(source, key, history=True):
    """按主键取单条错误记录；key 为含主键列的 dict，无结果返回 None。"""
    src = SOURCES[source]
    where = " AND ".join("%s = :%s" % (c, c) for c in src.key_cols)
    rows = _select(src, _all_cols(src), history, where, key, limit=1)
    return _normalize(src, rows[0]) if rows else None


def list_records(source, date, history=True, only_text=True, limit=None):
    """按日期取某来源的错误记录列表；only_text 仅保留报错文本非空的记录。"""
    src = SOURCES[source]
    where = "%s = :date" % src.date_col
    params = {"date": date}
    if only_text:
        where += " AND %s IS NOT NULL" % src.text_col
    rows = _select(src, _all_cols(src), history, where, params, limit)
    return [_normalize(src, d) for d in rows]


def list_by_date(date, sources=None, history=True, only_text=True):
    """跨来源取某日全部错误记录。"""
    out = []
    for sid in (sources or list(SOURCES)):
        out.extend(list_records(sid, date, history=history, only_text=only_text))
    return out


def sample_records(source, limit=100000, history=True):
    """跨日期取样（按日期倒序、文本非空），用于构建相似案例检索索引。"""
    src = SOURCES[source]
    sql = "SELECT %s FROM %s WHERE %s IS NOT NULL ORDER BY %s DESC LIMIT %d" % (
        ", ".join(_all_cols(src)), _table(src, history),
        src.text_col, src.date_col, int(limit))
    cols, rows = query(sql)
    return [_normalize(src, dict(zip(cols, r))) for r in rows]
