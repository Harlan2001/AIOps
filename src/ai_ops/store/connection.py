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
# 只读路径禁止出现的写/DDL 动词（含写 CTE 场景）。
_FORBIDDEN_READONLY_RE = re.compile(
    r"\b(insert|update|delete|drop|alter|truncate|create|grant|revoke|"
    r"merge|replace)\b", re.IGNORECASE)
# 从 SQL 中粗略提取被写的表名，用于校验是否为允许的日志表。
_TABLE_RE = {
    "insert": re.compile(r"^\s*insert\s+into\s+([A-Za-z0-9_.]+)", re.IGNORECASE),
    "update": re.compile(r"^\s*update\s+([A-Za-z0-9_.]+)", re.IGNORECASE),
}


class StoreWriteError(PermissionError):
    """写连接安全校验失败：非允许动词、非日志表或非法语句。"""


def _assert_readonly(sql):
    """只读契约：仅允许 SELECT / WITH 开头，且不含任何写或 DDL 动词。

    写 CTE（WITH x AS (DELETE ...) SELECT ...）因含 DELETE 被拒；
    DELETE/DROP/ALTER/TRUNCATE 等非 SELECT 开头语句直接拒绝。
    """
    s = sql.strip()
    low = s.lower()
    if not (low.startswith("select") or low.startswith("with")):
        raise StoreWriteError(
            "execute_select 仅允许 SELECT/WITH，已拒绝：" + s[:120])
    if _FORBIDDEN_READONLY_RE.search(low):
        raise StoreWriteError(
            "execute_select 检测到写/DDL 动词，已拒绝：" + s[:120])


def _assert_allowed(sql, table):
    m = _ALLOWED_WRITE_RE.match(sql.strip())
    if not m:
        raise StoreWriteError(
            "写连接仅允许 INSERT/UPDATE，已拒绝：" + sql[:120])
    verb = m.group(1).lower()
    tm = _TABLE_RE[verb].match(sql.strip())
    target = tm.group(1) if tm else ""
    # 允许带 schema 前缀（dimple.aiops_diag_log）或裸表名；比较时统一取
    # 最后一段表名，避免 table 配置带 schema 时被误判为越权。
    bare = target.split(".")[-1]
    expected_bare = table.split(".")[-1]
    if bare != expected_bare:
        raise StoreWriteError(
            "写连接仅允许操作日志表 %s，目标为 %s，已拒绝" % (table, target))


def _bind_write(sql, params):
    """写路径专用绑定：允许 None（驱动按 NULL 绑定），不套用只读路径的 None 硬校验。

    只读 `_db._bind` 拒绝 None 是为了防止缺参变成永假条件；写库时空值是合法列，
    因此这里保留 None 作为参数值，仅做 :name -> $1..$n 转换。
    """
    names = []
    for m in _db._NAME_RE.finditer(sql):
        name = m.group(1)
        if name not in names:
            names.append(name)
    idx = {name: i + 1 for i, name in enumerate(names)}
    pg_sql = _db._NAME_RE.sub(
        lambda m: "$%d" % idx[m.group(1)], sql)
    values = [(params or {}).get(name) for name in names]
    return pg_sql, values


def execute_write(sql, params, table):
    """执行参数化 INSERT/UPDATE（限定日志表），返回影响行数（不可得时返回 None）。"""
    _assert_allowed(sql, table)
    pg_sql, values = _bind_write(sql, params)
    conn = _db.get_conn()
    try:
        stmt = conn.prepare(pg_sql)
        cur = stmt(*values)
        return getattr(cur, "rowcount", None)
    finally:
        conn.close()


def execute_select(sql, params=None):
    """存储自身使用的只读查询，返回 (列名list, 行list)。"""
    _assert_readonly(sql)
    pg_sql, values = _db._bind(sql, params)
    conn = _db.get_conn()
    try:
        stmt = conn.prepare(pg_sql)
        rows = list(stmt(*values))
        cols = list(stmt.column_names or [])
    finally:
        conn.close()
    return cols, rows


def read_only_snapshot(queries):
    """在同一连接的只读事务中执行多条 SELECT，返回与 queries 对齐的 (cols, rows) 列表。

    用于聚合统计，保证各查询读到同一快照，避免并发写入导致口径不一致。
    """
    for sql, _p in queries:
        _assert_readonly(sql)
    conn = _db.get_conn()
    try:
        conn.prepare("BEGIN READ ONLY")()
        out = []
        try:
            for sql, params in queries:
                pg_sql, values = _db._bind(sql, params)
                stmt = conn.prepare(pg_sql)
                rows = list(stmt(*values))
                cols = list(stmt.column_names or [])
                out.append((cols, rows))
        except Exception:
            conn.prepare("ROLLBACK")()
            raise
        conn.prepare("COMMIT")()
        return out
    finally:
        conn.close()
