# -*- coding: utf-8 -*-
"""规则加载期 fail-fast 校验（阶段 3·②）：启动时用 977 表结构清单校验全部 runbook SQL。

设计：
- 与 tests/unit/test_runbook_integrity.py 共用同一份解析逻辑（单点事实源，避免测试与运行时漂移）；
- 表结构清单缺失时（如 wheel 交付不含 docs/）降级为 warning，不阻断启动；
- 校验失败时聚合报出全部错误，启动即拦截，替代"运行时静默降级"。
"""
import pathlib
import re
import warnings

from ai_ops import paths, rules_store

# 已安装态（wheel 交付、无源码仓库）探测不到 REPO_ROOT，且清单文档不随包分发：
# 此时置 None，由 catalog_available() 统一走“缺清单 -> warning 降级”。
# 切勿在此无条件拼接路径——REPO_ROOT 为 None 时 `None / "docs"` 会在 import 期
# 直接 TypeError，导致 Engine() 无法构造（降级守卫根本来不及执行）。
CATALOG = (
    paths.REPO_ROOT / "docs" / "error" / "GaussDB_dimple_全量表结构与字段含义清单.md"
    if paths.REPO_ROOT else None
)

# 提取 SQL 列引用时的非列白名单（同 test_runbook_integrity，保持一致）
SQL_NON_COL = {
    "count", "sum", "max", "min", "avg", "cast", "select", "from", "where",
    "order", "by", "group", "limit", "desc", "asc", "as", "dimple",
    "distinct", "like", "between", "in", "is", "null", "and", "or", "not",
    "on", "join", "left", "right", "exists", "bigint", "case", "when",
    "then", "else", "end",
}


def catalog_available(path=None):
    """表结构清单文档是否存在（wheel 交付可能不含 docs/，此时跳过 fail-fast）。"""
    p = path or CATALOG
    return bool(p) and p.is_file()


def load_catalog(path=None):
    """解析 `## N. dimple.<表> (<n> 字段)` 清单 -> {表名: {列名, ...}}。"""
    p = pathlib.Path(path or CATALOG)
    tables = {}
    cur = None
    for line in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## \d+\. dimple\.(\w+)\s*\(\d+ 字段\)$", line.strip())
        if m:
            cur = m.group(1)
            tables[cur] = set()
            continue
        if cur and line.strip().startswith("|") and not line.strip().startswith("|---"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and cells[0] and cells[0] != "字段名":
                tables[cur].add(cells[0])
    return tables


def sql_tables_and_cols(sql):
    """提取 SQL 引用的表名与列名（宽松解析，供存在性校验）。"""
    s = re.sub(r"'[^']*'", "''", sql)
    tables = re.findall(r"from\s+dimple\.(\w+)", s, re.I)
    cols = set()
    m = re.search(r"select\s+(.+?)\s+from\s+dimple\.(\w+)", s, re.I)
    if m:
        for seg in m.group(1).split(","):
            seg = re.sub(r"^(\w+)\(", "", seg.strip())
            seg = re.split(r"\s+as\s+", seg, flags=re.I)[0].strip()
            seg = re.sub(r"\(.*\)", "", seg).strip()
            if re.match(r"^[A-Za-z_]\w*$", seg):
                cols.add(seg)
    for m2 in re.finditer(r"\b([a-z_]\w*)\s*(?:=|>=|<=|<>|!=|>|<)", s, re.I):
        cols.add(m2.group(1))
    # ORDER BY / GROUP BY 子句中的列（N9：此前不解析，坏列可漏过校验）
    for clause in re.findall(
            r"(?:order|group)\s+by\s+(.+?)(?:\blimit\b|$)", s, re.I | re.S):
        for token in re.findall(r"[A-Za-z_]\w*", clause):
            # 标识符统一小写（GaussDB 未加引号标识符折叠为小写；DESC/ASC 等关键字亦然）
            cols.add(token.lower())
    return tables, cols


def validate_runbook(rb_id, rb, tables=None):
    """校验单个 runbook 的每条 SQL 表/列与清单一致，返回错误列表 [{step_id, msg}]。"""
    if tables is None:
        tables = load_catalog()
    errors = []
    for step in rb.get("steps", []):
        sql = step.get("sql") or ""
        sid = step.get("id")
        tbls, cols = sql_tables_and_cols(sql)
        if not tbls:
            errors.append({"step": sid,
                           "msg": "%s step %s 未引用 dimple. 表: %s" % (rb_id, sid, sql[:80])})
            continue
        for t in tbls:
            if t not in tables:
                errors.append({"step": sid,
                               "msg": "%s step %s 引用清单外表 dimple.%s（SQL: %s）"
                                      % (rb_id, sid, t, sql[:80])})
                continue
            for c in cols:
                if c in SQL_NON_COL:
                    continue
                if c not in tables[t]:
                    errors.append({"step": sid,
                                   "msg": "%s step %s 引用清单外列 %s.%s（SQL: %s）"
                                          % (rb_id, sid, t, c, sql[:80])})
    return errors


def validate_all_errors():
    """校验 errors.yaml 引用的全部 runbook，返回聚合错误列表（含 warn 兼容检查）。"""
    types = rules_store.load_registries()[0]
    errors = []
    for t in types:
        rb_name = t.get("runbook")
        if not rb_name:
            continue
        rb = rules_store.load_runbook(rb_name)
        errors.extend(validate_runbook(rb_name, rb))
    return errors


def ensure_valid():
    """加载期 fail-fast 入口：清单缺失 -> warning 降级；校验失败 -> RuntimeError（启动即拦截）。"""
    if not catalog_available():
        warnings.warn(
            "表结构清单缺失（%s），跳过规则加载期 fail-fast 校验，"
            "运行时降级仍会显式可见（sql_errors）。" % CATALOG)
        return
    errors = validate_all_errors()
    if errors:
        lines = ["规则加载期校验失败（%d 处 SQL 引用与 977 表清单不一致，拒绝启动）："
                 % len(errors)]
        lines += ["  - %s" % e["msg"] for e in errors[:50]]
        if len(errors) > 50:
            lines.append("  ... 其余 %d 处省略" % (len(errors) - 50))
        raise RuntimeError("\n".join(lines))
