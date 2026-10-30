# -*- coding: utf-8 -*-
"""API 契约测试：固化 service 层与 FastAPI 薄壳的对齐（前后端共用同一服务面）。

覆盖：/healthz、/v1/diagnose、/v1/batch-diagnose、/v1/records、/v1/rules。
设计原则：核心断言不依赖外部库可达（诊断类型识别在库不可用时仍成立）。
"""
import pytest
from fastapi.testclient import TestClient

from ai_ops.api import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["rules_count"] >= 15
    assert body["noise_keywords"] > 0
    assert "gauss" in body and "msg" in body["gauss"]
    assert "time" in body


def test_diagnose_text_hits_type(client):
    """文本模式：规则引擎识别类型（不依赖库可达，取证失败也应命中）。"""
    r = client.post("/v1/diagnose", json={
        "text": "[合约=>Au(T+D)]结算价不存在", "ldate": "20250305"})
    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "text"
    assert body["result"]["class"] == "biz"
    assert body["result"]["type"]["id"] == "settle_price_not_found"
    assert body["result"]["verdict"] == "诊断完成"


def test_diagnose_empty_text_422(client):
    r = client.post("/v1/diagnose", json={"text": ""})
    assert r.status_code == 422


def test_diagnose_unknown_source_404(client):
    r = client.post("/v1/diagnose", json={"record": {"source": "nope", "key": {}}})
    assert r.status_code == 404
    assert "未知错误来源" in r.json()["detail"]


def test_batch_diagnose_noise_and_biz(client):
    """批量：噪音自动过滤 + 业务报错命中类型（与页面 diagnose_many 同一服务）。"""
    r = client.post("/v1/batch-diagnose", json={"items": [
        {"text": "处理成功"},
        {"text": "平仓错误,[会员=>016811][客户=>0000000168][合约=>Au(T+N1)][买]持仓不足,尚缺<3>",
         "ldate": "20250304"},
    ]})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 2
    assert body["results"][0]["result"]["class"] == "noise"
    assert body["results"][1]["result"]["class"] == "biz"
    assert body["results"][1]["result"]["type_id"] == "position_not_enough"


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
