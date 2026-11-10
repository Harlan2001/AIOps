# -*- coding: utf-8 -*-
"""API 契约测试（D1 方案 C）：固化统一 DiagnosisResult 契约与升级/熔断行为。

覆盖：/healthz、/v1/diagnose（默认零 token / 可选升级 / 409 / 降级）、
/v1/batch-diagnose、/v1/records、/v1/rules。
设计原则：不依赖外部库可达；升级用 mock LLM 注入，escalation_allowed 显式打桩，
保证本地与 CI 行为一致，不触发真实外网。
"""
import pytest
from fastapi.testclient import TestClient

from ai_ops.api import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def svc(client):
    return app.state.service


class FakeLLM:
    """可控 LLM：ok=True 返回兜底结论；ok=False 模拟未配置/不可用（返回 None）。"""

    def __init__(self, ok=True):
        self._ok = ok
        self.calls = 0

    def diagnose(self, ctx):
        self.calls += 1
        if not self._ok:
            return None
        return {"root": "LLM 兜底根因（mock）",
                "actions": ["LLM 兜底处置动作（mock）"],
                "confidence": 0.7, "secondary": []}

    def available(self):
        return self._ok


# 不匹配任何中文关键词、也非噪音的无意义文本，确保规则未识别
UNMATCHED_TEXT = "glorkx zworp vogon 7771"


def test_healthz(client, monkeypatch):
    # 打桩 GaussDB 探测，避免依赖真实网络（CI 无法路由内网地址）
    monkeypatch.setattr(
        app.state.service, "check_gauss",
        lambda *a, **k: {"ok": True, "msg": "mock 可达", "checked": "00:00:00"})
    r = client.get("/healthz")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["gauss"]["ok"] is True
    assert body["rules_count"] >= 15
    assert body["noise_keywords"] > 0
    assert "msg" in body["gauss"]
    assert "time" in body


def test_healthz_degraded_when_gauss_down(client, monkeypatch):
    # GaussDB 不可达：HTTP 仍 200，顶层 status=degraded（N4）
    monkeypatch.setattr(
        app.state.service, "check_gauss",
        lambda *a, **k: {"ok": False, "msg": "mock 不可达", "checked": "00:00:00"})
    r = client.get("/healthz")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "degraded"
    assert body["gauss"]["ok"] is False


def test_diagnose_default_rule_only_zero_token(client, svc):
    """默认 escalate=false：纯规则零 token，kb_card=null，返回统一契约形状。"""
    r = client.post("/v1/diagnose", json={
        "text": "[合约=>Au(T+D)]结算价不存在", "ldate": "20250305"})
    assert r.status_code == 200
    body = r.json()
    # 契约不变量
    assert body["escalated"] is False
    assert body["kb_card"] is None
    assert isinstance(body["loc"], str)
    assert isinstance(body["answer"]["actions"], list)
    assert body["rule_res"]["type"]["id"] == "settle_price_not_found"
    assert body["rule_res"]["verdict"] == "诊断完成"
    assert "零 token" in body["source"]


def test_diagnose_empty_text_422(client):
    r = client.post("/v1/diagnose", json={"text": ""})
    assert r.status_code == 422


def test_diagnose_unknown_source_404(client):
    r = client.post("/v1/diagnose", json={"record": {"source": "nope", "key": {}}})
    assert r.status_code == 404
    assert "未知错误来源" in r.json()["detail"]


def test_diagnose_escalate_llm_fallback_success(client, svc, monkeypatch):
    """escalate=true 且规则未覆盖：走到 mock LLM 兜底，200 且 escalated=true。"""
    fake = FakeLLM(ok=True)
    monkeypatch.setattr(svc, "llm", fake)
    monkeypatch.setattr(svc, "escalation_allowed", lambda: True)

    r = client.post("/v1/diagnose", json={"text": UNMATCHED_TEXT, "escalate": True})
    assert r.status_code == 200
    body = r.json()
    assert body["escalated"] is True
    assert fake.calls == 1
    assert "LLM" in body["source"]
    assert body["answer"]["root"] == "LLM 兜底根因（mock）"
    assert body["answer"]["actions"] == ["LLM 兜底处置动作（mock）"]


def test_diagnose_escalate_llm_unavailable_graceful_200(client, svc, monkeypatch):
    """escalate=true 但 LLM 未配置/不可用：200 优雅降级，source 标注兜底来源。"""
    fake = FakeLLM(ok=False)
    monkeypatch.setattr(svc, "llm", fake)
    monkeypatch.setattr(svc, "escalation_allowed", lambda: True)

    r = client.post("/v1/diagnose", json={"text": UNMATCHED_TEXT, "escalate": True})
    assert r.status_code == 200
    body = r.json()
    assert body["escalated"] is True
    assert "兜底" in body["source"]
    assert body["answer"] is not None
    assert body["answer"]["root"]


def test_diagnose_escalate_disabled_409(client, svc, monkeypatch):
    """部署未允许升级：escalate=true 直接 409，可审计、不静默。"""
    monkeypatch.setattr(svc, "escalation_allowed", lambda: False)

    r = client.post("/v1/diagnose", json={"text": UNMATCHED_TEXT, "escalate": True})
    assert r.status_code == 409
    assert "未启用 LLM 升级" in r.json()["detail"]


def test_batch_diagnose_contract_shape(client):
    """批量默认纯规则：逐条为统一契约，噪音/业务均可识别。"""
    r = client.post("/v1/batch-diagnose", json={"items": [
        {"text": "处理成功"},
        {"text": "平仓错误,[会员=>016811][客户=>0000000168][合约=>Au(T+N1)][买]持仓不足,尚缺<3>",
         "ldate": "20250304"},
    ]})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 2
    first = body["results"][0]["result"]
    second = body["results"][1]["result"]
    assert first["escalated"] is False and first["kb_card"] is None
    assert second["rule_res"]["type"]["id"] == "position_not_enough"
    assert isinstance(second["answer"]["actions"], list)


def test_batch_diagnose_escalate_disabled_409(client, svc, monkeypatch):
    """批量条目要求升级而部署不允许：整体 409。"""
    monkeypatch.setattr(svc, "escalation_allowed", lambda: False)
    r = client.post("/v1/batch-diagnose", json={"items": [
        {"text": UNMATCHED_TEXT, "escalate": True}]})
    assert r.status_code == 409


def test_batch_diagnose_requires_input_422(client):
    r = client.post("/v1/batch-diagnose", json={})
    assert r.status_code == 422


def test_rules_list(client):
    r = client.get("/v1/rules")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] >= 15
    assert "noise_keywords" in body
    assert body["rules"][0]["id"] and body["rules"][0]["runbook"]
