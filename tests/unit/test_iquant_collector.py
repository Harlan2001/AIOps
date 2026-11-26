# -*- coding: utf-8 -*-
"""iQuant 采集器单元测试（离线打桩，不连真实环境与 GaussDB）。"""
import json

import pytest

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


class PersistErrorService:
    """诊断成功但数据库临时故障：服务层用内部标记告知采集层。"""

    def diagnose_many_isolated(self, recs, escalate_flags=None, _ctx=None):
        return [(r, {"rule_res": {}, "answer": {},
                     "_persist_error": "db down"}) for r in recs]

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


def test_diagnose_error_not_marked_and_retried(monkeypatch, tmp_path):
    monkeypatch.setattr(C, "load_iquant_config", lambda: _enabled_cfg())
    pages = [{"retCode": 200000, "total": 1,
              "data": [_raw_event(1, "NEW")]}]
    cur_path = tmp_path / "c.json"

    s1 = C.run_realtime_collection(
        svc=ErrorService(), client=FakeClient(pages),
        cursor=C.CursorStore(path=cur_path))
    assert s1["errors"] == 1
    assert s1["diagnosed"] == 0

    # 故障恢复后同一事件必须重试，而不是因上轮失败被永久跳过。
    s2 = C.run_realtime_collection(
        svc=FakeService(), client=FakeClient(pages),
        cursor=C.CursorStore(path=cur_path))
    assert s2["diagnosed"] == 1
    assert s2["skipped_seen"] == 0

    s3 = C.run_realtime_collection(
        svc=FakeService(), client=FakeClient(pages),
        cursor=C.CursorStore(path=cur_path))
    assert s3["diagnosed"] == 0
    assert s3["skipped_seen"] == 1


def test_persist_error_not_marked_and_retried(monkeypatch, tmp_path):
    monkeypatch.setattr(C, "load_iquant_config", lambda: _enabled_cfg())
    pages = [{"retCode": 200000, "total": 1,
              "data": [_raw_event(1, "NEW")]}]
    cur_path = tmp_path / "c.json"

    s1 = C.run_realtime_collection(
        svc=PersistErrorService(), client=FakeClient(pages),
        cursor=C.CursorStore(path=cur_path))
    assert s1["errors"] == 1
    assert s1["diagnosed"] == 0

    s2 = C.run_realtime_collection(
        svc=FakeService(), client=FakeClient(pages),
        cursor=C.CursorStore(path=cur_path))
    assert s2["diagnosed"] == 1
    assert s2["skipped_seen"] == 0


def test_skipped_closed_can_be_reprocessed_after_config_change(monkeypatch, tmp_path):
    cfg = _enabled_cfg(handle_closed=False)
    monkeypatch.setattr(C, "load_iquant_config", lambda: dict(cfg))
    pages = [{"retCode": 200000, "total": 1,
              "data": [_raw_event(2, "HANDLED")]}]
    cur_path = tmp_path / "c.json"

    s1 = C.run_realtime_collection(
        svc=FakeService(), client=FakeClient(pages),
        cursor=C.CursorStore(path=cur_path))
    assert s1["skipped_closed"] == 1
    assert s1["diagnosed"] == 0

    cfg["handle_closed"] = True
    s2 = C.run_realtime_collection(
        svc=FakeService(), client=FakeClient(pages),
        cursor=C.CursorStore(path=cur_path))
    assert s2["skipped_seen"] == 0
    assert s2["diagnosed"] == 1


def test_missing_event_id_is_invalid_not_seen(monkeypatch, tmp_path):
    monkeypatch.setattr(C, "load_iquant_config", lambda: _enabled_cfg())
    pages = [{"retCode": 200000, "total": 1,
              "data": [_raw_event(None, "NEW")]}]
    s = C.run_realtime_collection(
        svc=FakeService(), client=FakeClient(pages),
        cursor=C.CursorStore(path=tmp_path / "c.json"))
    assert s["fetched"] == 1
    assert s["invalid"] == 1
    assert s["skipped_seen"] == 0
    assert s["diagnosed"] == 0
    assert s["errors"] == 0


def test_max_pages_truncation_is_reported(monkeypatch, tmp_path):
    monkeypatch.setattr(
        C, "load_iquant_config",
        lambda: _enabled_cfg(page_size=1, max_pages=1))
    pages = [
        {"retCode": 200000, "total": 2, "data": [_raw_event(1, "NEW")]},
        {"retCode": 200000, "total": 2, "data": [_raw_event(2, "NEW")]},
    ]
    client = FakeClient(pages)
    s = C.run_realtime_collection(
        svc=FakeService(), client=client,
        cursor=C.CursorStore(path=tmp_path / "c.json"))
    assert s["fetched"] == 1
    assert s["diagnosed"] == 1
    assert s["truncated"] is True
    assert s["by_endpoint"][EP.id]["total"] == 2
    assert s["by_endpoint"][EP.id]["truncated"] is True
    assert s["by_endpoint"][EP.id]["page_next"] == 2
    assert len(client.calls) == 1

    # 下一轮从持久化的第 2 页继续，尾部事件不会永远采不到。
    s2 = C.run_realtime_collection(
        svc=FakeService(), client=FakeClient(pages),
        cursor=C.CursorStore(path=tmp_path / "c.json"))
    assert s2["diagnosed"] == 1
    assert s2["truncated"] is False
    assert s2["by_endpoint"][EP.id]["page_start"] == 2
    assert s2["by_endpoint"][EP.id]["page_next"] == 1


def test_cursor_is_reloaded_after_lock(monkeypatch, tmp_path):
    monkeypatch.setattr(C, "load_iquant_config", lambda: _enabled_cfg())
    path = tmp_path / "c.json"
    # 模拟 worker B 在等待锁之前加载的空游标；worker A 随后写入成功指纹。
    stale = C.CursorStore(path=path)
    pages = [{"retCode": 200000, "total": 1,
              "data": [_raw_event(1, "NEW")]}]
    s1 = C.run_realtime_collection(
        svc=FakeService(), client=FakeClient(pages),
        cursor=C.CursorStore(path=path))
    assert s1["diagnosed"] == 1

    s2 = C.run_realtime_collection(
        svc=FakeService(), client=FakeClient(pages), cursor=stale)
    assert s2["diagnosed"] == 0
    assert s2["skipped_seen"] == 1


def test_malformed_row_is_isolated(monkeypatch, tmp_path):
    monkeypatch.setattr(C, "load_iquant_config", lambda: _enabled_cfg())
    pages = [{"retCode": 200000, "total": 2,
              "data": [None, _raw_event(1, "NEW")]}]
    s = C.run_realtime_collection(
        svc=FakeService(), client=FakeClient(pages),
        cursor=C.CursorStore(path=tmp_path / "c.json"))
    assert s["invalid"] == 1
    assert s["diagnosed"] == 1
    assert s["errors"] == 0


@pytest.mark.parametrize("payload", ["[]", "1", '"bad"', '{"seen": []}'])
def test_invalid_cursor_shape_raises(payload, tmp_path):
    path = tmp_path / "c.json"
    path.write_text(payload, encoding="utf-8")
    with pytest.raises(C.CursorStoreError):
        C.CursorStore(path=path)


def test_invalid_cursor_aborts_without_replaying(monkeypatch, tmp_path):
    monkeypatch.setattr(C, "load_iquant_config", lambda: _enabled_cfg())
    path = tmp_path / "c.json"
    path.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(C, "state_file", lambda _name: path)
    client = FakeClient([
        {"retCode": 200000, "total": 1, "data": [_raw_event(1, "NEW")]}])
    s = C.run_realtime_collection(svc=FakeService(), client=client)
    assert s["status"] == "error"
    assert s["error"] == "cursor_load_failed"
    assert client.calls == []


def test_success_fingerprint_does_not_expire_by_default(tmp_path):
    path = tmp_path / "c.json"
    cursor = C.CursorStore(path=path)
    fp = C._event_fingerprint(EP, 1)
    cursor._seen[fp] = 1.0  # 远早于任何默认 TTL 的历史成功记录
    cursor.save()
    assert C.CursorStore(path=path).seen(fp) is True
    # 只有显式配置 TTL 才清理；调用方需自行接受历史事件重放风险。
    assert C.CursorStore(path=path, ttl_days=1).seen(fp) is False


def test_interprocess_lock_excludes_second_acquirer(tmp_path):
    path = tmp_path / "c.json.lock"
    first, second = C._InterProcessLock(path), C._InterProcessLock(path)
    assert first.acquire() is True
    assert second.acquire() is False
    first.release()
    assert second.acquire() is True
    second.release()


def test_locked_run_skips_upstream_and_diagnosis(monkeypatch, tmp_path):
    monkeypatch.setattr(C, "load_iquant_config", lambda: _enabled_cfg())
    cursor = C.CursorStore(path=tmp_path / "c.json")
    lock = C._InterProcessLock(
        cursor.path.with_name(cursor.path.name + ".lock"))
    assert lock.acquire() is True
    try:
        client = FakeClient([
            {"retCode": 200000, "total": 1, "data": [_raw_event(1, "NEW")]}])
        s = C.run_realtime_collection(
            svc=FakeService(), client=client, cursor=cursor)
        assert s["status"] == "locked"
        assert client.calls == []
    finally:
        lock.release()


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
