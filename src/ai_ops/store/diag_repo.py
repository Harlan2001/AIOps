# -*- coding: utf-8 -*-
"""诊断日志领域仓储（方向一·阶段 0）。

职责：
  - build_fingerprint：sha256 去重指纹，保证巡检重复执行不重复记账；
  - build_entry：把诊断记录 + 契约结果 + 触发上下文映射为日志表行；
  - save_log / upsert_log：参数化写入（写连接限定日志表）。

本模块只做数据映射与落库，不做开关判断（开关在 persist 门面）。
"""
import hashlib
import json
import re
import uuid
from datetime import date, datetime
from decimal import Decimal

from ..config import load_config
from . import connection

DEFAULT_TABLE = "aiops_diag_log"
_WS_RE = re.compile(r"\s+")

# 正常业务数据来源（行情/持仓/资金/库存/委托/成交/申报等），不是异常。
# 口径须与 dimple.collector.BUSINESS_ENDPOINTS 保持一致；store 层不反向导入
# collector 以避免循环依赖，故在此独立声明。这些 id 均为内部固定常量，
# 可安全内联进 SQL（无注入风险）。
BUSINESS_SOURCES = {
    "dimple_trader_order", "dimple_member_order",
    "dimple_real_time_quot", "dimple_real_time_arbi_quot",
    "dimple_integrate_posi", "dimple_trade_purpose_posi",
    "dimple_member_hold", "dimple_self_run_trader_hold",
    "dimple_rfq_posi",
    "dimple_fund_realtime", "dimple_estimate_account_remain",
    "dimple_member_inventory", "dimple_self_run_trader_stock",
    "dimple_estimate_storage_remain", "dimple_client_storage_flow",
    "dimple_self_run_trader_deal", "dimple_member_transaction",
    "dimple_rfq_match", "dimple_rfq_uncheck_match",
    "dimple_defer_fee_rate", "dimple_member_qty_weight_limit",
    "dimple_trader_qty_weight_limit",
    "dimple_option_exec", "dimple_self_hedging",
    "dimple_trader_delivery_declare",
    "dimple_trader_delivery_declare_trade",
    "dimple_rfq_default_declaration",
}


# 额度与限额 ifOver 表示"超限/成立"的取值；采集层与历史查询共用同一口径。
QUOTA_OVER_TOKENS = {"1", "1.0", "true", "y", "yes", "是", "超限"}


def _anomaly_cond():
    """返回"仅真实异常"的 SQL 片段：
      1) 排除业务数据来源（行情/持仓/资金/库存等）；
      2) 额度限额按 ifOver 渲染值做真值白名单过滤，与采集层保持一致；
    source 为空的早期演示数据保留。不物理删除，业务数据仍可回溯。"""
    in_list = ", ".join("'%s'" % s for s in sorted(BUSINESS_SOURCES))
    quota_over = " OR ".join(
        "LOWER(TRIM(error_text)) LIKE '%%是否超限 %s'" % token
        for token in sorted(QUOTA_OVER_TOKENS))
    return (
        "(source IS NULL OR source NOT IN (%s)) "
        "AND (source IS NULL OR source <> 'dimple_quota_and_limit' "
        "OR (%s))" % (in_list, quota_over))


def _realtime_cond():
    """实时监控来源：Dimple（dimple_ 前缀）或 iQuant（iquant_ 前缀），两者前缀均为 7 字符。"""
    return ("(SUBSTR(source, 1, 7) = 'dimple_' "
            "OR SUBSTR(source, 1, 7) = 'iquant_')")


def _json_default(o):
    """JSON 兜底：GaussDB NUMERIC 返回 Decimal，时间字段返回 datetime/date。"""
    if isinstance(o, Decimal):
        return float(o)
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    raise TypeError("不可 JSON 序列化的类型：%s" % type(o).__name__)


def _dumps(obj):
    return json.dumps(obj, ensure_ascii=False, default=_json_default)


def load_table():
    """读取配置的日志表名，缺省回退 DEFAULT_TABLE。"""
    cfg = load_config("store")
    return cfg.get("table") or DEFAULT_TABLE


def _norm_text(text):
    return _WS_RE.sub(" ", (text or "").strip())


def build_fingerprint(trigger_type, source, business_date, text, key_json):
    """构造确定性去重指纹：触发类型 + 来源 + 业务日期 + 规范化文本 + 主键 JSON。"""
    raw = "|".join([
        trigger_type or "",
        source or "",
        business_date or "",
        _norm_text(text),
        key_json or "",
    ])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def build_entry(rec, out, trigger_type, batch_id=None,
                diag_status="success", error_msg=None):
    """把诊断输入/输出映射为日志表行 dict。

    rec：诊断记录（text/ldate/errcode/source/key 等）；
    out：契约结果（envelope，含 rule_res/answer/escalated）；
    trigger_type：manual / manual_batch / scheduled。
    """
    rule_res = out.get("rule_res") or {}
    answer = out.get("answer") or {}
    tcfg = rule_res.get("type")
    diag_type = tcfg.get("id") if isinstance(tcfg, dict) else None
    key = rec.get("key")
    key_json = (
        json.dumps(key, ensure_ascii=False, sort_keys=True, default=_json_default)
        if key else None)
    text = rec.get("text") or ""
    source = rec.get("source") or None
    business_date = rec.get("ldate") or None
    base_fingerprint = build_fingerprint(
        trigger_type, source, business_date, text, key_json)
    # 巡检用确定性指纹做 upsert 去重；手工/批量事件允许重复，每次为独立事件，
    # 追加随机 nonce 使指纹唯一，避免唯一约束冲突或被合并覆盖。
    if trigger_type == "scheduled":
        fingerprint = base_fingerprint
    else:
        fingerprint = hashlib.sha256(
            (base_fingerprint + uuid.uuid4().hex).encode("utf-8")).hexdigest()
    escalated = bool(out.get("escalated"))

    return {
        "batch_id": batch_id,
        "trigger_type": trigger_type,
        "input_mode": "record" if source else "text",
        "source": source,
        "business_date": business_date,
        "error_text": text,
        "error_code": rec.get("errcode") or 0,
        "key_json": key_json,
        "fingerprint": fingerprint,
        "diag_class": rule_res.get("class"),
        "diag_type": diag_type,
        "root_cause": answer.get("root"),
        "confidence": answer.get("confidence"),
        "diag_path": "escalated" if escalated else "rule",
        "escalated": escalated,
        "evidence_count": len(rule_res.get("evidence") or []),
        "result_json": _dumps(out),
        "diag_status": diag_status,
        "error_msg": error_msg,
    }


_INSERT_COLS = [
    "batch_id", "trigger_type", "input_mode", "source", "business_date",
    "error_text", "error_code", "key_json", "fingerprint", "diag_class",
    "diag_type", "root_cause", "confidence", "diag_path", "escalated",
    "evidence_count", "result_json", "diag_status", "error_msg",
]


def _insert_sql(table):
    cols = ", ".join(_INSERT_COLS)
    params = ", ".join(":" + c for c in _INSERT_COLS)
    return "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, params)


def save_log(entry, table=None):
    """普通插入（指纹冲突时由库唯一约束报错）。"""
    table = table or load_table()
    return connection.execute_write(_insert_sql(table), entry, table)


def upsert_log(entry, table=None):
    """插入；指纹冲突时更新为最新结论，避免巡检重复记账。

    本 GaussDB 内核不支持 PG 的 ON CONFLICT，改用其兼容的 MySQL 风格
    ON DUPLICATE KEY UPDATE（VALUES(col) 引用待插入值）。
    结论被替换时，旧的人工标注（状态/正确答案/标注人/时间）一并清空，
    避免新结论被误认为仍已人工确认。
    """
    table = table or load_table()
    update_cols = [c for c in _INSERT_COLS
                   if c not in ("fingerprint", "trigger_type")]
    set_clause = ", ".join("%s = VALUES(%s)" % (c, c) for c in update_cols)
    set_clause += (
        ", annot_status = NULL, correct_answer = NULL, "
        "annotator = NULL, annotated_at = NULL")
    sql = _insert_sql(table) + " ON DUPLICATE KEY UPDATE " + set_clause
    return connection.execute_write(sql, entry, table)


# ============================================================================
# M2：历史查询与聚合（只读）
# ============================================================================

# 列表返回的列（不含可能很大的 result_json，详情才取）。
_LIST_COLS = [
    "id", "batch_id", "trigger_type", "input_mode", "source", "business_date",
    "error_text", "diag_class", "diag_type", "root_cause", "confidence",
    "diag_path", "escalated", "evidence_count", "diag_status",
    "annot_status", "correct_answer", "annotator", "annotated_at", "created_at",
]


def _rows_to_dicts(cols, rows):
    return [dict(zip(cols, r)) for r in rows]


def list_logs(table=None, source=None, diag_class=None, diag_type=None,
              annot_status=None, start_date=None, end_date=None,
              offset=0, limit=50, exclude_business=False, dimple_only=False,
              realtime_only=False):
    """按条件分页查询历史诊断（按业务日期倒序，最新在前），返回 {total, items}。

    exclude_business=True：叠加"仅真实异常"过滤，排除业务数据与未超限记录。
    dimple_only=True：仅查询 Dimple 来源（保留向后兼容）。
    realtime_only=True：查询全部实时监控来源（Dimple 或 iQuant），供统一实时页使用，
    避免手工/历史巡检记录混入。
    历史页开关默认均为 False，可查看全部落库记录。
    """
    table = table or load_table()
    where, params = [], {}
    if dimple_only:
        where.append("SUBSTR(source, 1, 7) = 'dimple_'")
    if realtime_only:
        where.append(_realtime_cond())
    if exclude_business:
        where.append(_anomaly_cond())

    def add(cond, name, value):
        key = name
        where.append(cond % key)
        params[key] = value

    if source:
        add("source = :%s", "source", source)
    if diag_class:
        add("diag_class = :%s", "diag_class", diag_class)
    if diag_type:
        add("diag_type = :%s", "diag_type", diag_type)
    if annot_status:
        add("annot_status = :%s", "annot_status", annot_status)
    if start_date:
        add("business_date >= :%s", "start_date", start_date)
    if end_date:
        add("business_date <= :%s", "end_date", end_date)

    where_sql = (" WHERE " + " AND ".join(where)) if where else ""
    _, total_rows = connection.execute_select(
        "SELECT COUNT(*) AS cnt FROM %s%s" % (table, where_sql), params)
    total = int(total_rows[0][0])

    qparams = dict(params)
    qparams["offset"] = int(offset)
    qparams["limit"] = max(1, min(int(limit), 200))
    cols_sql = ", ".join(_LIST_COLS)
    # 主排序按业务日期（页面展示的时间），最新在前；无业务日期的手工记录置末。
    # 同一业务日期内再按落库时间、id 倒序兜底，保证分页稳定。
    list_sql = (
        "SELECT %s FROM %s%s "
        "ORDER BY business_date DESC NULLS LAST, created_at DESC, id DESC "
        "LIMIT :limit OFFSET :offset"
        % (cols_sql, table, where_sql))
    cols, rows = connection.execute_select(list_sql, qparams)
    return {"total": total, "items": _rows_to_dicts(cols, rows)}


def get_log(log_id, table=None):
    """取单条完整记录（含 result_json）；无结果返回 None。"""
    table = table or load_table()
    cols, rows = connection.execute_select(
        "SELECT * FROM %s WHERE id = :log_id" % table,
        {"log_id": int(log_id)})
    rows = _rows_to_dicts(cols, rows)
    return rows[0] if rows else None


def update_annotation(log_id, annot_status, correct_answer, annotator, table=None):
    """更新人工标注（含标注人留痕与标注时间），返回影响行数。"""
    table = table or load_table()
    sql = (
        "UPDATE %s SET annot_status = :annot_status, "
        "correct_answer = :correct_answer, annotator = :annotator, "
        "annotated_at = CURRENT_TIMESTAMP WHERE id = :log_id" % table)
    params = {
        "annot_status": annot_status,
        "correct_answer": correct_answer,
        "annotator": annotator,
        "log_id": int(log_id),
    }
    return connection.execute_write(sql, params, table)


def stats(table=None, start_date=None, end_date=None, top_n=10):
    """聚合统计：总量、按日趋势、高频类型 TOP、分类分布、升级/异常率、标注量。

    所有查询在同一连接的只读事务中执行，保证各口径属于同一快照，
    避免并发写入导致分类合计与 total 不一致、异常率越界。
    """
    table = table or load_table()
    # 基础条件始终包含"仅真实异常"过滤，业务数据不进任何统计口径。
    where, params = [_anomaly_cond()], {}
    if start_date:
        where.append("business_date >= :start_date")
        params["start_date"] = start_date
    if end_date:
        where.append("business_date <= :end_date")
        params["end_date"] = end_date
    base_where = " WHERE " + " AND ".join(where)

    def filter_sql(extra):
        # 已有过滤条件时用 AND 追加；否则以 WHERE 起头。
        if base_where:
            return base_where + " AND " + extra
        return " WHERE " + extra

    def group_sql(group_col, order, extra_params=None, limit=False):
        sql = (
            "SELECT %s AS grp, COUNT(*) AS cnt FROM %s%s GROUP BY %s ORDER BY %s"
            % (group_col, table, base_where, group_col, order))
        p = dict(params)
        if limit:
            sql += " LIMIT :top"
            p["top"] = int(top_n)
        if extra_params:
            p.update(extra_params)
        return sql, p

    def count_sql(extra):
        return "SELECT COUNT(*) AS cnt FROM %s%s" % (
            table, filter_sql(extra)), dict(params)

    queries = [
        ("SELECT COUNT(*) AS cnt FROM %s%s" % (table, base_where), dict(params)),
        group_sql("business_date", "grp"),
        group_sql("diag_type", "cnt DESC", limit=True),
        group_sql("diag_class", "grp"),
        count_sql("escalated = TRUE"),
        count_sql("diag_status = 'error'"),
        count_sql("annot_status IS NOT NULL"),
    ]
    results = connection.read_only_snapshot(queries)

    def groups(idx):
        return [{"key": r[0], "count": int(r[1])}
                for r in results[idx][1]]

    total = int(results[0][1][0][0])
    escalated = int(results[4][1][0][0])
    abnormal = int(results[5][1][0][0])
    return {
        "total": total,
        "by_date": groups(1),
        "top_types": groups(2),
        "by_class": groups(3),
        "escalated": escalated,
        "abnormal": abnormal,
        # 同一快照下 abnormal <= total，比率不会超过 1；total=0 时归零。
        "abnormal_rate": (abnormal / total) if total else 0.0,
        "annotated": int(results[6][1][0][0]),
    }
