# -*- coding: utf-8 -*-
"""方向一·阶段 1 定时巡检单元测试（离线、打桩，不连真实 GaussDB）。"""
import pytest

from ai_ops.scheduler import inspector, runner


class FakeService:
    def __init__(self, raise_on=None):
        self.raise_on = raise_on
        self.calls = []

    def sources(self):
        return {"ftr_err": "期货错误委托"}

    def list_records(self, source, date, history=True, limit=None, offset=0):
        self.calls.append(("list", source, date, limit, history, offset))
        if self.raise_on and date == self.raise_on:
            raise RuntimeError("db unavailable")
        return [{"text": "a", "ldate": date}, {"text": "b", "ldate": date}]

    def count_records(self, source, date, history=True):
        return 2

    def diagnose_many_isolated(self, recs, escalate_flags=None, _ctx=None):
        self.calls.append(("diag", len(recs), _ctx))
        return [(r, {"rule_res": {}, "answer": {}}) for r in recs]


_ENABLED = {
    "enabled": True, "interval_minutes": 120, "cron": "",
    "sources": ["ftr_err"], "lookback_days": 1, "batch_size": 200,
}


def test_disabled_returns_disabled(monkeypatch):
    monkeypatch.setattr(inspector, "load_schedule",
                        lambda: {"enabled": False})
    assert run()["status"] == "disabled"


def run(**kw):
    return inspector.run_inspection(**kw)


def test_inspection_flow(monkeypatch):
    monkeypatch.setattr(inspector, "load_schedule", lambda: dict(_ENABLED))
    fake = FakeService()
    summary = run(svc=fake)
    assert summary["status"] == "ok"
    assert len(summary["batch_id"]) == 32
    assert summary["scanned"] == 2
    assert summary["diagnosed"] == 2
    assert summary["errors"] == 0
    # 诊断上下文标记为定时巡检并带批次号
    diag_calls = [c for c in fake.calls if c[0] == "diag"]
    assert diag_calls[0][2] == {
        "trigger_type": "scheduled", "batch_id": summary["batch_id"]}


def test_inspection_isolates_source_error(monkeypatch):
    monkeypatch.setattr(inspector, "load_schedule", lambda: dict(_ENABLED))
    fake = FakeService(raise_on=_ENABLED_dates(monkeypatch))
    summary = run(svc=fake)
    assert summary["scanned"] == 0
    # 取数失败计入 fetch_errors，不与诊断失败混淆，diagnosed 不会为负
    assert summary["fetch_errors"] == 1
    assert summary["errors"] == 0
    assert summary["diagnosed"] == 0
    assert summary["by_source"]["ftr_err"]["fetch_errors"] == 1


def _ENABLED_dates(monkeypatch):
    # 让唯一的目标日期触发异常
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d")


def test_inspection_skips_when_locked(monkeypatch):
    monkeypatch.setattr(inspector, "load_schedule", lambda: dict(_ENABLED))
    assert inspector._RUN_LOCK.acquire(blocking=False)
    try:
        assert run(svc=FakeService())["status"] == "skipped"
    finally:
        inspector._RUN_LOCK.release()


class PagedService:
    """模拟分页：按 offset 返回 batch_size 条，超过总数返回空。"""

    def __init__(self, total):
        self.total = total
        self.history_seen = []

    def sources(self):
        return {"ftr_err": "期货错误委托"}

    def list_records(self, source, date, history=True, limit=None, offset=0):
        self.history_seen.append(history)
        remain = self.total - offset
        if remain <= 0:
            return []
        n = min(limit, remain)
        return [{"text": "r%d" % (offset + i), "ldate": date}
                for i in range(n)]

    def count_records(self, source, date, history=True):
        return self.total

    def diagnose_many_isolated(self, recs, escalate_flags=None, _ctx=None):
        return [(r, {"rule_res": {}, "answer": {}}) for r in recs]


def test_today_uses_today_table_and_paginates(monkeypatch):
    from datetime import datetime
    cfg = dict(_ENABLED, batch_size=2, max_scan_per_source=5000)
    monkeypatch.setattr(inspector, "load_schedule", lambda: cfg)
    fake = PagedService(total=5)
    summary = inspector.run_inspection(svc=fake)
    # 当天日期 history=False，且分 3 页读全（2+2+1）
    assert set(fake.history_seen) == {False}
    assert summary["scanned"] == 5
    assert summary["truncated"] is False
    assert summary["unscanned"] == 0


def test_pagination_truncated_reports_unscanned(monkeypatch):
    cfg = dict(_ENABLED, batch_size=2, max_scan_per_source=4)
    monkeypatch.setattr(inspector, "load_schedule", lambda: cfg)
    fake = PagedService(total=10)
    summary = inspector.run_inspection(svc=fake)
    assert summary["truncated"] is True
    assert summary["scanned"] == 4
    assert summary["unscanned"] == 6


def test_init_error_releases_lock(monkeypatch):
    # batch_size 非法导致初始化抛错，锁仍须释放，后续巡检不会永久 skipped
    cfg = dict(_ENABLED, batch_size="abc")
    monkeypatch.setattr(inspector, "load_schedule", lambda: cfg)
    with pytest.raises(ValueError):
        inspector.run_inspection(svc=FakeService())
    assert inspector._RUN_LOCK.acquire(blocking=False)
    inspector._RUN_LOCK.release()


def test_build_scheduler_none_when_disabled(monkeypatch):
    monkeypatch.setattr(inspector, "load_schedule",
                        lambda: {"enabled": False})
    assert runner.build_scheduler() is None


def test_build_scheduler_interval_and_cron(monkeypatch):
    monkeypatch.setattr(inspector, "load_schedule", lambda: dict(_ENABLED))
    sched = runner.build_scheduler()
    job = sched.get_job("aiops_inspection")
    assert job is not None
    assert job.max_instances == 1

    cron_cfg = dict(_ENABLED, cron="0 18 * * *")
    monkeypatch.setattr(inspector, "load_schedule", lambda: cron_cfg)
    sched_cron = runner.build_scheduler()
    assert sched_cron.get_job("aiops_inspection") is not None


def test_api_lifespan_scheduler_disabled_by_default():
    from fastapi.testclient import TestClient

    from ai_ops.api import app
    with TestClient(app) as client:
        # 默认未启用巡检，调度器应为 None，服务仍正常
        assert client.app.state.scheduler is None
        resp = client.get("/healthz")
        assert resp.status_code == 200
