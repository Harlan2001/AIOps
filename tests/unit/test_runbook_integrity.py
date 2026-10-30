# -*- coding: utf-8 -*-
"""runbook 完整性 + 表结构一致性（阶段 1 固本）。

把此前手工校验（review_check / sql_check）固化为回归测试：
  1. 全部 runbook / errors.yaml / noise_rules.yaml 可 safe_load；
  2. errors.yaml 20 类型 <-> runbooks 20 个映射完整、无多余文件、文件名=id；
  3. steps 结构完整（sql_check 必有 expect，type 合法）；
  4. 每个 runbook 有 default；
  5. SQL 无 Oracle 残留（CLEAR./ULOG./INTERFACE. schema、TO_CHAR、FETCH FIRST）；
  6. 每条 SQL 的表名/列名均在 docs/error 全量表结构清单中；
  7. SQL 绑定参数 :name 均有来源（extra_params / param_alias / 记录业务列 / 默认日期）。
"""
import pathlib
import re

import pytest
import yaml

from ai_ops import paths, rules_store

RULES = pathlib.Path(rules_store.__file__).parent / "assets" / "rules"
CATALOG = paths.REPO_ROOT / "docs" / "error" / "GaussDB_dimple_全量表结构与字段含义清单.md"

# ---------- 1) YAML 可加载 ----------

RUNBOOK_FILES = sorted((RULES / "runbooks").glob("rb_*.yaml"))


@pytest.fixture(scope="module")
def runbooks():
    loaded = {}
    for f in RUNBOOK_FILES:
        rb = yaml.safe_load(f.read_text(encoding="utf-8"))
        assert isinstance(rb, dict) and rb.get("id"), f"{f.name} 缺 id"
        loaded[rb["id"]] = (f.name, rb)
    return loaded


def test_registry_yamls_loadable():
    yaml.safe_load((RULES / "errors.yaml").read_text(encoding="utf-8"))
    yaml.safe_load((RULES / "noise_rules.yaml").read_text(encoding="utf-8"))


# ---------- 2) types <-> runbooks 映射 ----------

def test_types_runbook_mapping_complete(runbooks):
    types = yaml.safe_load((RULES / "errors.yaml").read_text(encoding="utf-8"))["types"]
    assert len(types) == 20  # 与改造文档声明一致（原 3 → 20）
    missing = [t["id"] for t in types if t.get("runbook") not in runbooks]
    assert missing == [], f"types 引用不存在的 runbook: {missing}"
    # 无多余 runbook：每个文件都必须被某个 type 引用
    referenced = {t["runbook"] for t in types if t.get("runbook")}
    extra = set(runbooks) - referenced
    assert extra == set(), f"存在未被引用的 runbook: {extra}"


def test_runbook_filename_matches_id(runbooks):
    for rb_id, (fn, _rb) in runbooks.items():
        assert fn == rb_id + ".yaml", f"{rb_id} 的文件名应为 {rb_id}.yaml，实际 {fn}"


# ---------- 3) steps 结构 ----------

def test_steps_structure(runbooks):
    for rb_id, (fn, rb) in runbooks.items():
        assert rb.get("steps"), f"{fn} 无 steps"
        for i, s in enumerate(rb["steps"]):
            miss = {"id", "title", "type", "sql"} - set(s)
            assert not miss, f"{fn} step{i} 缺字段 {miss}"
            assert s["type"] in ("sql_check", "sql_query"), \
                f"{fn} step {s['id']} 未知 type: {s['type']}"
            if s["type"] == "sql_check":
                assert "expect" in s, f"{fn} step {s['id']} 是 sql_check 但缺 expect"


def test_default_exists(runbooks):
    for rb_id, (fn, rb) in runbooks.items():
        assert "default" in rb, f"{fn} 缺 default"
        assert rb["default"].get("root"), f"{fn} default 缺 root"


# ---------- 4) 无 Oracle 残留 ----------

ORACLE_PATTERNS = [
    (r"\bCLEAR\.", "Oracle CLEAR schema"),
    (r"\bULOG\.", "Oracle ULOG schema"),
    (r"\bINTERFACE\.", "Oracle INTERFACE schema"),
    (r"\bTO_CHAR\b", "Oracle TO_CHAR"),
    (r"\bFETCH\s+FIRST\b", "Oracle FETCH FIRST"),
]


def test_no_oracle_sql(runbooks):
    for rb_id, (fn, rb) in runbooks.items():
        for s in rb["steps"]:
            sql = s.get("sql") or ""
            for pat, desc in ORACLE_PATTERNS:
                assert not re.search(pat, sql, re.I), \
                    f"{fn} step {s['id']} 含 {desc}: {sql}"


# ---------- 5) SQL 表名/列名与 977 表清单一致 ----------

def _load_catalog():
    tables = {}
    cur = None
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
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


def _sql_tables_and_cols(sql):
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
    return tables, cols


_SQL_NON_COL = {
    "count", "sum", "max", "min", "avg", "cast", "select", "from", "where",
    "order", "by", "group", "limit", "desc", "asc", "as", "dimple",
    "distinct", "like", "between", "in", "is", "null", "and", "or", "not",
    "on", "join", "left", "right", "exists", "bigint", "case", "when",
    "then", "else", "end",
}


def test_sql_tables_columns_exist_in_catalog(runbooks):
    tables = _load_catalog()
    assert len(tables) > 900, f"清单解析异常，仅 {len(tables)} 张表"
    checked = 0
    for rb_id, (fn, rb) in runbooks.items():
        for s in rb["steps"]:
            sql = s.get("sql") or ""
            tbls, cols = _sql_tables_and_cols(sql)
            assert tbls, f"{fn} step {s['id']} 未引用 dimple. 表: {sql}"
            for t in tbls:
                assert t in tables, f"{fn} step {s['id']} 引用清单外表 dimple.{t}"
                for c in cols:
                    if c in _SQL_NON_COL:
                        continue
                    assert c in tables[t], \
                        f"{fn} step {s['id']} 引用清单外列 {t}.{c}（SQL: {sql[:80]}）"
            checked += 1
    assert checked >= 50, f"核对 SQL 过少: {checked}"


# ---------- 6) SQL 绑定参数有来源 ----------

_BIND_RE = re.compile(r"(?<!:):([A-Za-z_]\w*)")


def test_sql_bind_params_have_source(runbooks):
    types = yaml.safe_load((RULES / "errors.yaml").read_text(encoding="utf-8"))["types"]
    t_by_runbook = {t.get("runbook"): t for t in types}
    for rb_id, (fn, rb) in runbooks.items():
        tcfg = t_by_runbook.get(rb_id, {})
        extra = set((rb.get("extra_params") or {}).keys())
        alias = set((tcfg.get("param_alias") or {}).values())
        for s in rb["steps"]:
            for name in _BIND_RE.findall(s.get("sql") or ""):
                has_src = (
                    name in ("trade_date", "ldate")      # 默认日期
                    or name in extra                      # runbook extra_params
                    or name in alias                      # errors.yaml param_alias
                    or name in {                            # 常见业务短名
                        "member", "client", "trader", "contract", "exch",
                        "variety", "market", "purpose", "bs", "eo", "user",
                        "flow_code", "oper_name", "alarm_type", "risk_type",
                        "seq_no", "local_no", "match_no", "trader_no",
                        "invest_id", "qty", "price", "bs_dir",
                    }
                )
                assert has_src, f"{fn} step {s['id']} 参数 :{name} 无明确来源"
