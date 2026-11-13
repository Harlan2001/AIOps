# -*- coding: utf-8 -*-
"""持久化写连接（方向一·阶段 0）。

与引擎只读 `engine/db.py` 的区别：
  - 引擎 `query()` 只允许 SELECT，且用于诊断取证；
  - 本模块提供独立的写连接，仅允许对诊断日志表执行参数化 INSERT/UPDATE，
    以及供本存储自身使用的 SELECT；写操作必须命中配置的日志表名，
    任何越权写、DDL 或对其他表的写都直接拒绝。

复用 engine.db 的命名参数绑定（:name -> $1..$n）与连接建立，避免重复实现。
"""
import re

from ..engine import db as _db

# 仅允许的写动词；DDL/DELETE/其他动词一律拒绝。
_ALLOWED_WRITE_RE = re.compile(r"^\s*(insert|update)\b", re.IGNORECASE)
# 从 SQL 中粗略提取被写的表名，用于校验是否为允许的日志表。
_TABLE_RE = {
    "insert": re.compile(r"^\s*insert\s+into\s+([A-Za-z0-9_.]+)", re.IGNORECASE),
    "update": re.compile(r"^\s*update\s+([A-Za-z0-9_.]+)", re.IGNORECASE),
}


class StoreWriteError(PermissionError):
    """写连接安全校验失败：非允许动词、非日志表或非法语句。"""


def _assert_allowed(sql, table):
    m = _ALLOWED_WRITE_RE.match(sql.strip())
    if not m:
        raise StoreWriteError(
            "写连接仅允许 INSERT/UPDATE，已拒绝：" + sql[:120])
    verb = m.group(1).lower()
    tm = _TABLE_RE[verb].match(sql.strip())
    target = tm.group(1) if tm else ""
    # 允许带 schema 前缀（dimple.aiops_diag_log）或裸表名。
    bare = target.split(".")[-1]
    if bare != table:
        raise StoreWriteError(
            "写连接仅允许操作日志表 %s，目标为 %s，已拒绝" % (table, target))


def execute_write(sql, params, table):
    """执行参数化 INSERT/UPDATE（限定日志表），返回影响行数（不可得时返回 None）。"""
    _assert_allowed(sql, table)
    pg_sql, values = _db._bind(sql, params)
    conn = _db.get_conn()
    try:
        stmt = conn.prepare(pg_sql)
        cur = stmt(*values)
        return getattr(cur, "rowcount", None)
    finally:
        conn.close()


def execute_select(sql, params=None):
    """存储自身使用的只读查询，返回 (列名list, 行list)。"""
    if _ALLOWED_WRITE_RE.match(sql.strip()):
        raise StoreWriteError("execute_select 不允许写操作：" + sql[:120])
    pg_sql, values = _db._bind(sql, params)
    conn = _db.get_conn()
    try:
        stmt = conn.prepare(pg_sql)
        rows = list(stmt(*values))
        cols = list(stmt.column_names or [])
    finally:
        conn.close()
    return cols, rows
