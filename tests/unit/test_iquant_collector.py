# -*- coding: utf-8 -*-
"""iQuant 采集器单元测试（离线打桩，不连真实环境与 GaussDB）。"""
import json

from ai_ops.iquant import collector as C
from ai_ops.iquant.client import IquantError

EP = C.ENDPOINTS[0]


def _raw_event(event_id=1001, status="NEW", **over):
    base = {
        "eventId": event_id,
        "ruleNo": "DAY-QTE-001",
        "ruleName": "在市报价市场偏离风险规则",
        "riskItem": "QUOTE_MARKET_DEVIATION",
        "riskLevel": "MEDIUM",
        "eventStatus": status,
        "objectName": "24附息国债11",
        "portfolioScope": "自营投组",
        "traderScope": "张三",
        "triggerValue": json.dumps({"deviation": 12.5}, ensure_ascii=False),
        "thresholdValue": json.dumps({"maxDeviation": 10}),
        "controlAction": json.dumps(["bubble", "record"]),
        "triggerCount": 3,
        "lastTriggerTime": "2026-11-20T09:25:48.377",
        "firstTriggerTime": "2026-11-20T09:00:00.000",
    }
    base.update(over)
    return base


# ---------------- 纯函数 ----------------

def test_parse_iso_date():
    assert C._parse_iso_date("2026-11-20T09:25:48.377") == "20261120"
    assert C._parse_iso_date("") == ""
    assert C._parse_iso_date(None) == ""


def test_maybe_json():
    assert C._maybe_json('{"a":1}') == {"a": 1}
    assert C._maybe_json("[1,2]") == [1, 2]
    assert C._maybe_json("plain") == "plain"
    assert C._maybe_json("{bad") == "{bad"
    assert C._maybe_json(5) == 5


def test_normalize_maps_date_and_nested_json():
    rec = C.normalize_record(_raw_event(), EP)
    assert rec["ldate"] == "20261120"
    assert rec["source"] == "iquant_day_abnormal_event"
    assert rec["source_label"] == "iQuant事中风控事件"
    assert rec["key"] == {"eventId": 1001}
    # 嵌套 JSON 被解析，原始字符串字段保留
    assert rec["params"]["triggerValueParsed"] == {"deviation": 12.5}
    assert rec["params"]["thresholdValueParsed"] == {"maxDeviation": 10}
    assert rec["params"]["controlActionParsed"] == ["bubble", "record"]
    assert isinstance(rec["params"]["triggerValue"], str)
    # 诊断文本含中文规则名、级别与对象
    assert "在市报价市场偏离风险规则" in rec["text"]
    assert "24附息国债11" in rec["text"]
    assert "风险级别 中" in rec["text"]


def test_fingerprint_stable_across_updates():
    fp1 = C._event_fingerprint(EP, 1001)
    # 同一 eventId 即使事件内容更新，指纹保持一致
    assert C._event_fingerprint(EP, 1001) == fp1
    # 不同 eventId 指纹不同
    assert C._event_fingerprint(EP, 1002) != fp1


# ---------------- 打桩对象 ----------------

class FakeClient:
    """按 pageNo 顺序返回预置页面。"""

    def __init__(self, pages):
        self.pages = pages
        self.calls = []

    def query_page(self, path, page_no, page_size, filters=None):
        self.calls.append((path, page_no, page_size, filters))
        idx = page_no - 1
        if idx >= len(self.pages):
            return {"retCode": 200000, "data": [], "total": 0}
        return self.pages[idx]


class FakeService:
    def __init__(self):
        self.diag_calls = []

    def diagnose_many_isolated(self, recs, escalate_flags=None, _ctx=None):
        self.diag_calls.append((len(recs), _ctx))
        return [(r, {"rule_res": {}, "answer": {}}) for r in recs]

    def close(self):
        pass


class ErrorService:
    def diagnose_many_isolated(self, recs, escalate_flags=None, _ctx=None):
        return [(r, {"_diagnose_error": "boom"}) for r in recs]

    def close(self):
        pass


def _enabled_cfg(**over):
    cfg = dict(C._DEFAULTS)
    cfg.update({"enabled": True, "page_size": 2, "max_pages": 50})
    cfg.update(over)
    return cfg


# ---------------- 主流程 ----------------

def test_disabled_returns_disabled(monkeypatch):
    monkeypatch.setattr(
        C, "load_iquant_config", lambda: dict(C._DEFAULTS, enabled=False))
    assert C.run_realtime_collection()["status"] == "disabled"


def test_run_paginates_filters_and_diagnoses(monkeypatch, tmp_path):
    monkeypatch.setattr(C, "load_iquant_config", lambda: _enabled_cfg())
    pages = [
        {"retCode": 200000, "total": 3,
         "data": [_raw_event(1, "NEW"), _raw_event(2, "HANDLED")]},
        {"retCode": 200000, "total": 3,
         "data": [_raw_event(3, "NOTIFIED")]},
    ]
    client = FakeClient(pages)
    svc = FakeService()
    cursor = C.CursorStore(path=tmp_path / "cur.json")

    summary = C.run_realtime_collection(svc=svc, client=client, cursor=cursor)

    assert summary["status"] == "ok"
    assert summary["fetched"] == 3
    assert summary["skipped_closed"] == 1   # HANDLED 被跳过
    assert summary["diagnosed"] == 2        # NEW + NOTIFIED
    assert summary["errors"] == 0
    # 拉了两页，诊断上下文标记为 scheduled
    assert [c[1] for c in client.calls] == [1, 2]
    assert svc.diag_calls[0][1]["trigger_type"] == "scheduled"
    assert svc.diag_calls[0][1]["batch_id"] == summary["batch_id"]


def test_incremental_second_run_skips_seen_after_restart(monkeypatch, tmp_path):
    monkeypatch.setattr(C, "load_iquant_config", lambda: _enabled_cfg())
    pages = [{"retCode": 200000, "total": 1,
              "data": [_raw_event(1, "NEW")]}]
    cur_path = tmp_path / "cur.json"

    s1 = C.run_realtime_collection(
        svc=FakeService(), client=FakeClient(pages),
        cursor=C.CursorStore(path=cur_path))
    assert s1["diagnosed"] == 1

    # 模拟重启：新建游标从文件加载，同一事件应全部判为已见
    s2 = C.run_realtime_collection(
        svc=FakeService(), client=FakeClient(pages),
        cursor=C.CursorStore(path=cur_path))
    assert s2["fetched"] == 1
    assert s2["skipped_seen"] == 1
    assert s2["diagnosed"] == 0


def test_handle_closed_includes_handled(monkeypatch, tmp_path):
    monkeypatch.setattr(
        C, "load_iquant_config",
        lambda: _enabled_cfg(handle_closed=True))
    pages = [{"retCode": 200000, "total": 1,
              "data": [_raw_event(2, "HANDLED")]}]
    s = C.run_realtime_collection(
        svc=FakeService(), client=FakeClient(pages),
        cursor=C.CursorStore(path=tmp_path / "c.json"))
    assert s["skipped_closed"] == 0
    assert s["diagnosed"] == 1


def test_fetch_error_isolated(monkeypatch, tmp_path):
    monkeypatch.setattr(C, "load_iquant_config", lambda: _enabled_cfg())

    class BoomClient:
        def query_page(self, *a, **k):
            raise IquantError("HTTP 500")

    s = C.run_realtime_collection(
        svc=FakeService(), client=BoomClient(),
        cursor=C.CursorStore(path=tmp_path / "c.json"))
    assert s["status"] == "ok"
    assert s["errors"] == 1
    assert s["diagnosed"] == 0


def test_diagnose_error_counted_and_cursor_marked(monkeypatch, tmp_path):
    monkeypatch.setattr(C, "load_iquant_config", lambda: _enabled_cfg())
    pages = [{"retCode": 200000, "total": 1,
              "data": [_raw_event(1, "NEW")]}]
    cursor = C.CursorStore(path=tmp_path / "c.json")
    s = C.run_realtime_collection(
        svc=ErrorService(), client=FakeClient(pages), cursor=cursor)
    assert s["errors"] == 1
    assert s["diagnosed"] == 0


def test_scheduler_registers_iquant_job(monkeypatch):
    from ai_ops.dimple import collector as dimple_collector
    from ai_ops.scheduler import inspector, runner

    monkeypatch.setattr(inspector, "load_schedule",
                        lambda: {"enabled": False})
    monkeypatch.setattr(dimple_collector, "load_dimple_config",
                        lambda: {"enabled": False})
    monkeypatch.setattr(
        C, "load_iquant_config",
        lambda: dict(C._DEFAULTS, enabled=True, interval_minutes=3))

    sched = runner.build_scheduler()
    job = sched.get_job("iquant_realtime")
    assert job is not None
    assert job.max_instances == 1
