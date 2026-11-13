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

from ..config import load_config
from . import connection

DEFAULT_TABLE = "aiops_diag_log"
_WS_RE = re.compile(r"\s+")


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
    key_json = json.dumps(key, ensure_ascii=False, sort_keys=True) if key else None
    text = rec.get("text") or ""
    source = rec.get("source") or None
    business_date = rec.get("ldate") or None
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
        "fingerprint": build_fingerprint(
            trigger_type, source, business_date, text, key_json),
        "diag_class": rule_res.get("class"),
        "diag_type": diag_type,
        "root_cause": answer.get("root"),
        "confidence": answer.get("confidence"),
        "diag_path": "escalated" if escalated else "rule",
        "escalated": escalated,
        "evidence_count": len(rule_res.get("evidence") or []),
        "result_json": json.dumps(out, ensure_ascii=False),
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
    """插入；指纹冲突时更新为最新结论，避免巡检重复记账。"""
    table = table or load_table()
    update_cols = [c for c in _INSERT_COLS if c not in ("fingerprint", "trigger_type")]
    set_clause = ", ".join("%s = EXCLUDED.%s" % (c, c) for c in update_cols)
    sql = _insert_sql(table) + " ON CONFLICT (fingerprint) DO UPDATE SET " + set_clause
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
              offset=0, limit=50):
    """按条件分页查询历史诊断（按 id 倒序），返回 {total, items}。"""
    table = table or load_table()
    where, params = [], {}

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
    list_sql = (
        "SELECT %s FROM %s%s ORDER BY id DESC LIMIT :limit OFFSET :offset"
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


def _group_count(table, group_col, params, extra_where="", top=None):
    sql = ("SELECT %s AS grp, COUNT(*) AS cnt FROM %s%s GROUP BY %s"
           % (group_col, table, extra_where, group_col))
    if top:
        sql += " ORDER BY cnt DESC LIMIT :top"
        params = dict(params, top=top)
    else:
        sql += " ORDER BY grp"
    _, rows = connection.execute_select(sql, params)
    return [{"key": r[0], "count": int(r[1])} for r in rows]


def stats(table=None, start_date=None, end_date=None, top_n=10):
    """聚合统计：总量、按日趋势、高频类型 TOP、分类分布、升级/降级率、标注量。"""
    table = table or load_table()
    where, params = [], {}
    if start_date:
        where.append("business_date >= :start_date")
        params["start_date"] = start_date
    if end_date:
        where.append("business_date <= :end_date")
        params["end_date"] = end_date
    where_sql = (" WHERE " + " AND ".join(where)) if where else ""

    _, total_rows = connection.execute_select(
        "SELECT COUNT(*) AS cnt FROM %s%s" % (table, where_sql), params)
    total = int(total_rows[0][0])

    out = {"total": total}
    if total == 0:
        out.update({"by_date": [], "top_types": [], "by_class": [],
                    "escalated": 0, "abnormal": 0, "abnormal_rate": 0.0,
                    "annotated": 0})
        return out

    out["by_date"] = _group_count(table, "business_date", dict(params), where_sql)
    out["top_types"] = _group_count(
        table, "diag_type", dict(params), where_sql, top=int(top_n))
    out["by_class"] = _group_count(table, "diag_class", dict(params), where_sql)

    _, esc_rows = connection.execute_select(
        "SELECT COUNT(*) AS cnt FROM %s%s AND escalated = TRUE"
        % (table, where_sql if where else " WHERE TRUE"), params)
    out["escalated"] = int(esc_rows[0][0])

    _, ab_rows = connection.execute_select(
        "SELECT COUNT(*) AS cnt FROM %s%s AND diag_status = 'error'"
        % (table, where_sql if where else " WHERE TRUE"), params)
    out["abnormal"] = int(ab_rows[0][0])
    out["abnormal_rate"] = out["abnormal"] / total

    _, an_rows = connection.execute_select(
        "SELECT COUNT(*) AS cnt FROM %s%s AND annot_status IS NOT NULL"
        % (table, where_sql if where else " WHERE TRUE"), params)
    out["annotated"] = int(an_rows[0][0])
    return out
