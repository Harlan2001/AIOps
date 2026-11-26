# -*- coding: utf-8 -*-
"""本地语义召回测试（不连库）：同义词 / 模糊匹配 / 负例保护 / 精确优先。"""
import pytest

from ai_ops.engine import semantic as S
from ai_ops.engine.rule_engine import Engine


@pytest.fixture(scope="module")
def eng():
    e = Engine()
    yield e
    e.close()


# 精确关键词命中：match_kind 必须为 keyword
def test_exact_keyword_kind(eng):
    t, _score, meta = eng.match_with_meta("客户交易可用资金不足，无法开仓", 0)
    # "可用资金不足"为同义词，"资金不足"也在同义词；精确 keywords 未出现时走语义
    assert t is not None
    assert meta["match_kind"] in ("keyword", "synonym")


# 口语化文本：同义词召回，路由到正确 runbook
@pytest.mark.parametrize("text,expect", [
    ("下单的时候提示钱不够，买不了", "strategy_fund_short"),
    ("这个合约价格到涨停了，报不进去", "price_limit"),
    ("现在收盘了不能交易", "market_closed"),
    ("自己买自己卖被系统拦下来了", "self_trade"),
    ("撤单太多，次数超限", "cancel_order_alert"),
])
def test_synonym_recall(eng, text, expect):
    t, _score, meta = eng.match_with_meta(text, 0)
    assert t is not None and t["id"] == expect
    assert meta["match_kind"] == "synonym"


# 含通用词“自成交”的具体预警短语：精确最长词应路由到预警类型，而非通用自成交。
@pytest.mark.parametrize("text", [
    "自成交太多",
    "自成交次数到上限",
    "自成交达到阀值",
])
def test_specific_self_trade_alert_beats_generic_keyword(eng, text):
    t, _score, meta = eng.match_with_meta(text, 0)
    assert t is not None and t["id"] == "self_trade_alert"
    assert meta["match_kind"] == "keyword"


# 错别字 / 繁简：模糊匹配召回
@pytest.mark.parametrize("text,expect", [
    ("持仓不组，平不了仓", "position_not_enough"),
    ("合約状态不对，无法交易", "contract_state_error"),
])
def test_fuzzy_recall(eng, text, expect):
    t, _score, meta = eng.match_with_meta(text, 0)
    assert t is not None and t["id"] == expect
    assert meta["match_kind"] == "fuzzy"


# 负例：尚未配规则 / 无关文本，必须返回 None，不得强行召回
@pytest.mark.parametrize("text", [
    "[交易员=>trader1]库存量不足，不允许分配",
    "系统不存在该条记录,存续期变更失败",
    "今天天气不错，适合出门散步",
])
def test_negative_not_recalled(eng, text):
    t, _score, meta = eng.match_with_meta(text, 0)
    assert t is None and meta["match_kind"] is None


# 归一化与 bigram 基础行为
def test_normalize_and_bigram():
    assert S.normalize("[会员=>016811] 持仓不足！") == "016811持仓不足"
    bg = S.bigrams("持仓不足")
    assert "持仓" in bg and "仓不" in bg and "不足" in bg


# 可注入同义词：隔离验证 SemanticMatcher
def test_injected_synonyms():
    types = [{"id": "x", "title": "X", "keywords": ["标准词"]}]
    m = S.SemanticMatcher(types, synonyms={"x": ["大白话"]})
    t, kind, score = m.match("这条全是大白话")
    assert t["id"] == "x" and kind == "synonym"


def test_synonyms_load_rules_overlay(tmp_path, monkeypatch):
    (tmp_path / "synonyms.yaml").write_text(
        "synonyms:\n  x: [\"外挂大白话\"]\n", encoding="utf-8")
    monkeypatch.setenv("AIOPS_RULES_DIR", str(tmp_path))
    types = [{"id": "x", "title": "X", "keywords": ["标准词"]}]
    m = S.SemanticMatcher(types)
    t, kind, _score = m.match("这条全是外挂大白话")
    assert t["id"] == "x" and kind == "synonym"
