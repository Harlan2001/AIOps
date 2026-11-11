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

from ai_ops import rules_store

RULES = pathlib.Path(rules_store.__file__).parent / "assets" / "rules"

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
# 解析逻辑与运行时 fail-fast 共用 schema_check（单点事实源）

def test_sql_tables_columns_exist_in_catalog(runbooks):
    from ai_ops.engine import schema_check as SC
    tables = SC.load_catalog()
    assert len(tables) > 900, f"清单解析异常，仅 {len(tables)} 张表"
    checked = 0
    for rb_id, (fn, rb) in runbooks.items():
        for s in rb["steps"]:
            sql = s.get("sql") or ""
            tbls, cols = SC.sql_tables_and_cols(sql)
            assert tbls, f"{fn} step {s['id']} 未引用 dimple. 表: {sql}"
            for t in tbls:
                assert t in tables, f"{fn} step {s['id']} 引用清单外表 dimple.{t}"
                for c in cols:
                    if c in SC.SQL_NON_COL:
                        continue
                    assert c in tables[t], \
                        f"{fn} step {s['id']} 引用清单外列 {t}.{c}（SQL: {sql[:80]}）"
            checked += 1
    assert checked >= 50, f"核对 SQL 过少: {checked}"


def test_schema_check_detects_bad_table_and_column():
    """fail-fast 校验核心：坏表/坏列/无表 SQL 均应报错（与运行时同源）。"""
    from ai_ops.engine import schema_check as SC
    tables = {"tt_ftr_order": {"order_no", "status", "qty"}}
    bad_table = {"id": "x", "steps": [
        {"id": "s1", "type": "sql_check", "sql": "select status from dimple.tt_nonexist where order_no = :no"}]}
    bad_col = {"id": "y", "steps": [
        {"id": "s1", "type": "sql_check", "sql": "select ghost_col from dimple.tt_ftr_order where status = :s"}]}
    no_table = {"id": "z", "steps": [
        {"id": "s1", "type": "sql_check", "sql": "select 1"}]}
    assert SC.validate_runbook("x", bad_table, tables), "坏表应报错"
    assert SC.validate_runbook("y", bad_col, tables), "坏列应报错"
    assert SC.validate_runbook("z", no_table, tables), "无表 SQL 应报错"
    good = {"id": "g", "steps": [
        {"id": "s1", "type": "sql_check",
         "sql": "select status from dimple.tt_ftr_order where order_no = :no"}]}
    assert SC.validate_runbook("g", good, tables) == [], "合法 SQL 不应报错"


def test_engine_warmup_failfast():
    """Engine 启动即校验：清单正常时实例化成功；校验失败时 RuntimeError。"""
    from ai_ops.engine import schema_check as SC
    from ai_ops.engine.rule_engine import Engine
    if not SC.catalog_available():
        pytest.skip("表结构清单缺失，跳过启动校验测试")
    Engine()  # 真实清单 + 20 runbook 应通过（不抛错）

    # 人为制造校验失败：替换校验函数返回错误 -> Engine 必须拒绝启动
    orig = SC.validate_runbook
    SC.validate_runbook = lambda rb_id, rb: [{"step": "s1", "msg": "人为注入：坏列"}]
    try:
        with pytest.raises(RuntimeError, match="规则加载期校验失败"):
            Engine()
    finally:
        SC.validate_runbook = orig


def test_engine_warmup_degrades_without_catalog(monkeypatch, tmp_path):
    """清单缺失时（wheel 交付不含 docs/）Engine 降级启动，不阻断。"""
    from ai_ops.engine import schema_check as SC
    from ai_ops.engine.rule_engine import Engine
    monkeypatch.setattr(SC, "CATALOG", tmp_path / "no_such_catalog.md")
    with pytest.warns(UserWarning, match="表结构清单缺失"):
        Engine()


# ---------- 6) SQL 绑定参数有来源（N9：收紧为动态来源，不再用无条件白名单） ----------

_BIND_RE = re.compile(r"(?<!:):([A-Za-z_]\w*)")


def test_sql_bind_params_have_source(runbooks):
    types = yaml.safe_load((RULES / "errors.yaml").read_text(encoding="utf-8"))["types"]
    t_by_runbook = {t.get("runbook"): t for t in types}

    # 允许的绑定名全部来自真实来源，动态构造，不硬编码兜底：
    # ① 默认日期；② 各 runbook extra_params；③ errors.yaml 全部 param_alias 值
    allowed = {"trade_date", "ldate"}
    for _rb_id, (_fn, rb) in runbooks.items():
        allowed.update((rb.get("extra_params") or {}).keys())
    for t in types:
        allowed.update((t.get("param_alias") or {}).values())

    for rb_id, (fn, rb) in runbooks.items():
        extra = set((rb.get("extra_params") or {}).keys())
        tcfg = t_by_runbook.get(rb_id, {})
        alias = set((tcfg.get("param_alias") or {}).values())
        for s in rb["steps"]:
            # 仅统计非注释行内的绑定参数
            sql_lines = [ln for ln in (s.get("sql") or "").splitlines()
                         if not ln.strip().startswith("#")]
            for name in _BIND_RE.findall("\n".join(sql_lines)):
                has_src = name in allowed or name in extra or name in alias
                assert has_src, f"{fn} step {s['id']} 参数 :{name} 无明确来源"


# ---------- 7) error_records 全部来源表/列在 977 清单内（N9：B1 类问题可被拦） ----------

def test_error_records_sources_exist_in_catalog():
    from ai_ops.engine import schema_check as SC
    from ai_ops.engine import error_records as ER

    catalog = SC.load_catalog()
    assert len(catalog) > 900
    for sid, src in ER.SOURCES.items():
        # 历史表：日期列、文本列、主键列、业务列均须在清单内
        assert src.his in catalog, f"来源 {sid} 历史表 dimple.{src.his} 不在清单"
        his_cols = catalog[src.his]
        for col in [src.date_col, src.text_col, *src.key_cols, *src.biz_cols]:
            assert col in his_cols, f"来源 {sid} 历史表缺列 {col}"

        # 当日表（部分来源无）：校验生效的当日日期列与主键列
        if not src.today:
            continue
        assert src.today in catalog, f"来源 {sid} 当日表 dimple.{src.today} 不在清单"
        today_cols = catalog[src.today]
        eff_date = ER.date_col_of(src, history=False)
        eff_keys = ER.key_cols_of(src, history=False)
        for col in [eff_date, src.text_col, *eff_keys]:
            assert col in today_cols, f"来源 {sid} 当日表缺列 {col}"
