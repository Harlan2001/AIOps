# -*- coding: utf-8 -*-
"""IquantClient 单元测试（离线打桩，不连真实环境）。"""
import json

import pytest

from ai_ops.iquant.client import (
    IquantClient, IquantError, LOGIN_SUCCESS, BIZ_SUCCESS_CODES)


def _make():
    return IquantClient(
        base_url="http://example:1080", username="admin",
        password="PlainSecret123", timeout=5)


def test_login_sends_plaintext_and_saves_token(monkeypatch):
    c = _make()
    captured = {}

    def fake_http(path, *, data=None, headers=None, method=None):
        captured.update(path=path, headers=headers, data=data)
        return {"retCode": LOGIN_SUCCESS,
                "result": {"access_token": "AT", "refresh_token": "RT",
                           "expires_in": 3600, "token_type": "bearer"}}

    monkeypatch.setattr(c, "_http", fake_http)
    assert c.login() == "AT"
    assert c._token == "AT" and c._refresh_token == "RT"
    # 走 /oauth/token 且带 Basic 客户端认证
    assert captured["path"] == "/oauth/token"
    assert captured["headers"]["Authorization"].startswith("Basic ")
    # 表单中密码为明文（原始密码直接出现），授权方式为 password
    form = captured["data"].decode()
    assert "password=PlainSecret123" in form
    assert "grant_type=password" in form


def test_login_raises_on_bad_credentials(monkeypatch):
    c = _make()
    monkeypatch.setattr(
        c, "_http",
        lambda *a, **k: {"retCode": "999999", "retMsg": "password incorrect"})
    with pytest.raises(IquantError):
        c.login()


def test_ensure_token_logins_then_refreshes(monkeypatch):
    c = _make()
    # 首次无 token -> 登录
    monkeypatch.setattr(c, "login", lambda: "FIRST")
    assert c.ensure_token() == "FIRST"

    # 已过期 -> 刷新
    c._token = "AT"
    c._expires_at = 0
    monkeypatch.setattr(c, "_do_refresh", lambda: "FRESH")
    assert c.ensure_token() == "FRESH"


def test_refresh_without_token_falls_back_to_login(monkeypatch):
    c = _make()
    c._token = "AT"
    c._refresh_token = None
    logged = []
    monkeypatch.setattr(c, "login", lambda: logged.append(1) or "AT")
    c._do_refresh()
    assert logged == [1]


def test_query_page_success_and_body_wraps_filters(monkeypatch):
    c = _make()
    c._token = "AT"
    monkeypatch.setattr(c, "ensure_token", lambda: "AT")
    captured = {}

    def fake_http(path, *, data=None, headers=None, method=None):
        captured["body"] = json.loads(data.decode())
        captured["headers"] = headers
        return {"retCode": 200000, "total": 1, "data": [{"eventId": 9}]}

    monkeypatch.setattr(c, "_http", fake_http)
    out = c.query_page(
        "/risk/dayAbnormalRiskEvent/queryTable", 2, 100,
        filters={"eventStatus": "NEW", "blank": "", "none": None})
    assert out["data"][0]["eventId"] == 9
    # 请求体结构：分页在顶层，筛选条件（空值已剔除）放入 data
    assert captured["body"]["pageNo"] == 2
    assert captured["body"]["pageSize"] == 100
    assert captured["body"]["data"] == {"eventStatus": "NEW"}
    # 业务请求带 Bearer 与 branch 头
    assert captured["headers"]["Authorization"] == "bearer AT"
    assert captured["headers"]["branch"] == "czbank"


def test_query_page_raises_on_business_error(monkeypatch):
    c = _make()
    c._token = "AT"
    monkeypatch.setattr(c, "ensure_token", lambda: "AT")
    monkeypatch.setattr(
        c, "_http", lambda *a, **k: {"retCode": 500, "retMsg": "boom"})
    with pytest.raises(IquantError):
        c.query_page("/x")


def test_query_page_retries_once_on_401(monkeypatch):
    c = _make()
    c._token = "OLD"
    monkeypatch.setattr(c, "ensure_token", lambda: c._token)
    auth_seen = []

    def fake_http(path, *, data=None, headers=None, method=None):
        auth_seen.append(headers["Authorization"])
        if len(auth_seen) == 1:
            raise IquantError("HTTP 401：Unauthorized")
        return {"retCode": 200000, "data": [], "total": 0}

    monkeypatch.setattr(c, "_http", fake_http)

    def do_login():
        c._token = "NEW"
        return "NEW"

    monkeypatch.setattr(c, "login", do_login)
    out = c.query_page("/x")
    assert out["retCode"] == 200000
    assert len(auth_seen) == 2
    assert auth_seen[0].endswith("OLD")
    assert auth_seen[1].endswith("NEW")


def test_biz_success_codes_cover_known_forms():
    # 兼容数字/字符串形态的成功码
    assert 200000 in BIZ_SUCCESS_CODES
    assert "200000" in BIZ_SUCCESS_CODES
    assert LOGIN_SUCCESS in BIZ_SUCCESS_CODES
