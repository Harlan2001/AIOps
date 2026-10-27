# -*- coding: utf-8 -*-
"""只读 GaussDB 连接封装（基于 py-opengauss，扩展协议 prepare，无需客户端）。

- 连接配置来自 config/db.yaml（经 ai_ops.config 加载，支持环境变量覆盖）
- 提供 query()：仅允许 SELECT；任何写操作直接拒绝
- 命名参数适配：上层/runbook 统一用 :name（Oracle 风格），本层转换为
  py-opengauss 的 $1/$2 位置参数；正确跳过 PG 的 :: 类型转换。
"""
import re

import py_opengauss

from ..config import load_config

_WRITE_RE = re.compile(
    r"^\s*(insert|update|delete|merge|create|drop|alter|truncate|grant|revoke|lock|comment)\b",
    re.IGNORECASE,
)
# :name 命名参数；(?<!:) 排除 :: 类型转换；参数名以字母/下划线开头
_NAME_RE = re.compile(r"(?<!:):([A-Za-z_]\w*)")
# 经 URL 连接时会破坏 userinfo / 权威段结构的字符（py-opengauss 不解析百分号编码，
# 这些字符无法用 %xx 绕过，遇到需直接报错，提示更换不含这些字符的账号口令）
_UNSAFE_RE = re.compile(r"[@:/?#]")


def _dsn(cfg):
    user, pwd = str(cfg["user"]), str(cfg["password"])
    for label, val in (("user", user), ("password", pwd)):
        if _UNSAFE_RE.search(val):
            raise ValueError(
                "config/db.yaml 的 %s 含 @ : / ? # 字符；py-opengauss 经 URL 连接且"
                "不解析百分号编码，无法使用，请改用不含这些字符的 %s" % (label, label))
    return "opengauss://%s:%s@%s:%s/%s" % (
        user, pwd, cfg["host"], cfg["port"], cfg["database"])


def get_conn():
    cfg = load_config("db", required=True)
    return py_opengauss.open(_dsn(cfg))


def _bind(sql, params):
    """把 :name 命名参数 SQL 转为 ($1..$n, 位置值)。"""
    names = []
    for m in _NAME_RE.finditer(sql):
        name = m.group(1)
        if name not in names:
            names.append(name)
    idx = {name: i + 1 for i, name in enumerate(names)}
    pg_sql = _NAME_RE.sub(lambda m: "$%d" % idx[m.group(1)], sql)
    values = [(params or {}).get(name) for name in names]
    return pg_sql, values


def query(sql, params=None, limit=None):
    """执行只读 SELECT，返回 (列名list, 行list)。"""
    if _WRITE_RE.match(sql.strip()):
        raise PermissionError("拒绝执行写操作，诊断引擎仅允许只读查询: " + sql[:120])
    pg_sql, values = _bind(sql, params)
    conn = get_conn()
    try:
        stmt = conn.prepare(pg_sql)
        rows = list(stmt(*values))
        cols = list(stmt.column_names or [])
    finally:
        conn.close()
    if limit:
        rows = rows[:limit]
    return cols, rows
