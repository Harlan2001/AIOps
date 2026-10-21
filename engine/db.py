# -*- coding: utf-8 -*-
"""只读 Oracle 连接封装（基于 python-oracledb thin 模式，无需客户端）。

- 连接配置来自 config/db.yaml
- 提供 query()：仅允许 SELECT；任何写操作直接拒绝
"""
import os
import re
import yaml
import oracledb

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_WRITE_RE = re.compile(
    r"^\s*(insert|update|delete|merge|create|drop|alter|truncate|grant|revoke|lock|comment)\b",
    re.IGNORECASE,
)


def load_db_config():
    with open(os.path.join(_ROOT, "config", "db.yaml"), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_conn():
    cfg = load_db_config()
    return oracledb.connect(user=cfg["user"], password=cfg["password"], dsn=cfg["dsn"])


def query(sql, params=None, limit=None):
    """执行只读 SELECT，返回 (列名list, 行list)。"""
    if _WRITE_RE.match(sql.strip()):
        raise PermissionError("拒绝执行写操作，诊断引擎仅允许只读查询: " + sql[:120])
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.arraysize = 1000
        cur.execute(sql, params or {})
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        if limit:
            rows = rows[:limit]
        return cols, rows
    finally:
        conn.close()
