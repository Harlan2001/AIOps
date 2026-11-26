# -*- coding: utf-8 -*-
"""iQuant 事中风控专用类型注册、自带证据 runbook 与统一置信度规则单元测试（离线，不连业务库）。"""
import pathlib

import pytest
import yaml

from ai_ops import pipeline, rules_store
from ai_ops.engine.rule_engine import Engine
from ai_ops.iquant import collector as C

RULES = pathlib.Path(rules_store.__file__).parent / "assets" / "rules"

IQUANT_TYPES = yaml.safe_load(
    (RULES / "iquant_errors.yaml").read_text(encoding="utf-8"))["types"]

# riskItem -> 期望的专用类型 id
RISK_ITEM_TO_TYPE = {
    "QUOTE_MARKET_DEVIATION": "iquant_quote_market_deviation",
    "POSITION_SWING": "iquant_position_swing",
    "MANUAL_PRICE_CHANGE": "iquant_manual_price_change",
    "ISSUER_CONCENTRATION": "iquant_issuer_concentration",
    "BULK_CLICK_DEAL": "iquant_bulk_click_deal",
    "SPECIAL_TRADE_MONITOR": "iquant_special_trade",
    "DEAL_TYPE_ABNORMAL": "iquant_deal_type_abnormal",
}


def _raw(risk_item):
    return {
        "eventId": "E-" + risk_item, "ruleNo": "DAY-X-001",
        "ruleName": "测试规则", "riskItem": risk_item,
        "objectName": "测试投组", "eventStatus": "NOTIFIED",
        "triggerValue": '{"a":1}', "thresholdValue": '{"b":0}',
        "controlAction": '["bubble"]', "triggerCount": 2,
        "lastTriggerTime": "2026-11-20T09:25:48.377",
    }


def test_iquant_registry_merged_into_types():
    types, _ = rules_store.load_registries()
    ids = {t["id"] for t in types}
    assert set(RISK_ITEM_TO_TYPE.values()) <= ids


def test_each_iquant_type_is_self_evidence_with_valid_runbook():
    assert len(IQUANT_TYPES) == 7
    for t in IQUANT_TYPES:
        assert t.get("self_evidence") is True
        # 置信度不写死在注册表里，统一由规则计算
        assert "confidence" not in t
        assert t.get("keywords")
        rb = rules_store.load_runbook(t["runbook"])
        assert rb["steps"] == []  # 自带证据，不跑业务 SQL
        assert rb["default"].get("root")
        assert rb["default"].get("action")


@pytest.fixture(scope="module")
def eng():
    return Engine()


def test_engine_classifies_all_iquant_items_with_confidence_1(eng):
    ep = C.ENDPOINTS[0]
    for risk_item, expected_type in RISK_ITEM_TO_TYPE.items():
        rec = C.normalize_record(_raw(risk_item), ep)
        res = eng.diagnose(rec)
        assert res["class"] == "biz"
        # 精确关键词命中，不再走 fuzzy 误路由到 Dimple 类型
        assert res["match_kind"] == "keyword"
        assert res["type"]["id"] == expected_type
        assert res["primary_evidence_ok"] is True
        # 精确命中 + 自带证据：统一规则给 1.0
        assert pipeline.rule_confidence(res) == 1.0
        assert res["root"]
        assert res["action"]


def test_position_swing_no_longer_fuzzy_routed_to_net_position_alert(eng):
    ep = C.ENDPOINTS[0]
    rec = C.normalize_record(_raw("POSITION_SWING"), ep)
    res = eng.diagnose(rec)
    assert res["type"]["id"] == "iquant_position_swing"
    assert res["type"]["id"] != "net_position_alert"


def test_self_evidence_bypass_requires_iquant_source(eng):
    # 手工文本即使命中 iQuant 关键词，也没有事件自带证据，不能直接给满分。
    res = eng.diagnose({"text": "交易头寸大幅波动", "errcode": 0, "params": {}})
    assert res["type"]["id"] == "iquant_position_swing"
    assert "self_evidence" not in res
    assert res["primary_evidence_ok"] is False
    assert pipeline.rule_confidence(res) == 0.4


# ---------- 统一置信度函数的真实档位（Dimple / iQuant 通用）----------

def test_rule_confidence_real_tiers():
    # 未识别类型（无 type）
    assert pipeline.rule_confidence({"type": None}) == 0.4
    # 同义词召回
    assert pipeline.rule_confidence({
        "type": {"id": "x"}, "match_kind": "synonym",
        "primary_evidence_ok": True}) == 0.8
    # 字符模糊召回
    assert pipeline.rule_confidence({
        "type": {"id": "x"}, "match_kind": "fuzzy",
        "primary_evidence_ok": True}) == 0.6
    # 精确关键词命中但主证据无成功取证
    assert pipeline.rule_confidence({
        "type": {"id": "x"}, "match_kind": "keyword",
        "primary_evidence_ok": False}) == 0.4
    # 语义召回同样不能绕过证据降级门
    assert pipeline.rule_confidence({
        "type": {"id": "x"}, "match_kind": "synonym",
        "primary_evidence_ok": False}) == 0.4
    assert pipeline.rule_confidence({
        "type": {"id": "x"}, "match_kind": "fuzzy",
        "primary_evidence_ok": False}) == 0.4
    # 精确关键词命中且主证据成功
    assert pipeline.rule_confidence({
        "type": {"id": "x"}, "match_kind": "keyword",
        "primary_evidence_ok": True}) == 1.0
