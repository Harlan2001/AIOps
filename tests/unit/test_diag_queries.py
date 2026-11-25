# -*- coding: utf-8 -*-
"""M2 历史诊断查询/聚合与 API 单元测试（离线打桩，不连真实 GaussDB）。"""
import json
import sqlite3

import pytest

from ai_ops.store import connection, diag_repo


class FakeSelect:
    """按 SQL 子串返回预置 (cols, rows)，并记录调用。"""

    def __init__(self):
        self.routes = []
        self.calls = []

    def add(self, key, cols, rows):
        self.routes.append((key, list(cols), [list(r) for r in rows]))

    def __call__(self, sql, params=None):
        self.calls.append((sql, params))
        # 选择最具体（键最长）的命中，避免通用键抢先匹配。
        matches = [(key, cols, rows) for key, cols, rows in self.routes
                   if key in sql]
        if matches:
            _key, cols, rows = max(matches, key=lambda m: len(m[0]))
            return cols, rows
        return ["x"], []


@pytest.fixture
def fake(monkeypatch):
    f = FakeSelect()
    monkeypatch.setattr(connection, "execute_select", f)
    return f


def test_list_logs_filters_and_paging(fake):
    fake.add("COUNT", ["cnt"], [[5]])
    fake.add("ORDER BY business_date DESC NULLS LAST, created_at DESC, id DESC", ["id", "source"], [[1, "ftr_err"], [2, None]])
    out = diag_repo.list_logs(source="ftr_err", offset=0, limit=10)
    assert out["total"] == 5
    assert len(out["items"]) == 2
    assert out["items"][0] == {"id": 1, "source": "ftr_err"}
    # 条件与分页参数被传入
    list_call = [c for c in fake.calls if "ORDER BY business_date DESC NULLS LAST, created_at DESC, id DESC" in c[0]][0]
    assert list_call[1]["source"] == "ftr_err"
    assert list_call[1]["limit"] == 10


def test_list_logs_dimple_only_combines_source_and_anomaly_filters(fake):
    fake.add("COUNT", ["cnt"], [[1]])
    fake.add("ORDER BY business_date DESC NULLS LAST, created_at DESC, id DESC", ["id"], [[1]])
    diag_repo.list_logs(dimple_only=True, exclude_business=True)

    assert len(fake.calls) == 2
    for sql, _params in fake.calls:
        assert "SUBSTR(source, 1, 7) = 'dimple_'" in sql
        assert "source IS NULL OR source NOT IN" in sql


def test_list_logs_realtime_only_matches_dimple_and_iquant(fake):
    fake.add("COUNT", ["cnt"], [[3]])
    fake.add("ORDER BY business_date DESC NULLS LAST, created_at DESC, id DESC", ["id"], [[1], [2], [3]])
    diag_repo.list_logs(realtime_only=True, exclude_business=True)

    assert len(fake.calls) == 2
    for sql, _params in fake.calls:
        # 同时包含 Dimple 与 iQuant 两个前缀条件
        assert "SUBSTR(source, 1, 7) = 'dimple_'" in sql
        assert "SUBSTR(source, 1, 7) = 'iquant_'" in sql
        assert "source IS NULL OR source NOT IN" in sql


def test_anomaly_sql_matches_collector_for_quota_values():
    """历史 SQL 与采集层对所有支持/拒绝的 ifOver 值必须给出相同结论。"""
    from ai_ops.dimple import collector

    values = [
        None, 0, 0.0, "0", "0.0", False, "False", "no", "unknown", "10",
        1, 1.0, "1", "1.0", True, "TRUE", "y", "YES", "是", "超限",
    ]
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE logs (id INTEGER, source TEXT, error_text TEXT)")
    for i, value in enumerate(values):
        rendered = "" if value is None else str(value)
        db.execute(
            "INSERT INTO logs VALUES (?, ?, ?)",
            (i, "dimple_quota_and_limit", "额度与限额：是否超限 " + rendered))

    expected = {
        i for i, value in enumerate(values)
        if collector.is_anomaly("dimple_quota_and_limit", {"ifOver": value})
    }
    actual = {
        row[0] for row in db.execute(
            "SELECT id FROM logs WHERE " + diag_repo._anomaly_cond()).fetchall()
    }
    assert actual == expected
    assert actual  # 同时覆盖真值，避免条件误写成全部排除


def test_get_log_found_and_missing(fake):
    fake.add("WHERE id", ["id", "diag_class"], [[7, "biz"]])
    assert diag_repo.get_log(7)["id"] == 7

    class Empty(FakeSelect):
        def __call__(self, sql, params=None):
            return ["id"], []

    fake2 = Empty()
    import ai_ops.store.connection as conn_mod
    conn_mod.execute_select = fake2
    assert diag_repo.get_log(999) is None


def test_stats_zero_total(monkeypatch):
    monkeypatch.setattr(connection, "read_only_snapshot", lambda q: [
        (["cnt"], [[0]]), (["grp", "cnt"], []), (["grp", "cnt"], []),
        (["grp", "cnt"], []), (["cnt"], [[0]]), (["cnt"], [[0]]),
        (["cnt"], [[0]]),
    ])
    out = diag_repo.stats()
    assert out["total"] == 0
    assert out["by_date"] == []
    assert out["abnormal_rate"] == 0.0


def test_stats_aggregation(monkeypatch):
    monkeypatch.setattr(connection, "read_only_snapshot", lambda q: [
        (["cnt"], [[10]]),
        (["grp", "cnt"], [["20250321", 6], ["20250320", 4]]),
        (["grp", "cnt"], [["fund", 8]]),
        (["grp", "cnt"], [["biz", 10]]),
        (["cnt"], [[2]]),
        (["cnt"], [[1]]),
        (["cnt"], [[3]]),
    ])
    out = diag_repo.stats(top_n=10)
    assert out["total"] == 10
    assert out["by_date"][0] == {"key": "20250321", "count": 6}
    assert out["top_types"][0] == {"key": "fund", "count": 8}
    assert out["escalated"] == 2
    assert out["abnormal"] == 1
    assert out["abnormal_rate"] == pytest.approx(0.1)
    assert out["annotated"] == 3


# ---------- API 行为 ----------


def test_api_stats_200_and_503(monkeypatch):
    from fastapi.testclient import TestClient

    from ai_ops.api import app
    from ai_ops.store import diag_repo as repo

    with TestClient(app) as client:
        monkeypatch.setattr(repo, "stats", lambda **k: {"total": 1})
        r = client.get("/v1/diagnoses/stats")
        assert r.status_code == 200
        assert r.json()["total"] == 1

        def _boom(**k):
            raise RuntimeError("table missing")

        monkeypatch.setattr(repo, "stats", _boom)
        r503 = client.get("/v1/diagnoses/stats")
        assert r503.status_code == 503


def test_api_detail_404(monkeypatch):
    from fastapi.testclient import TestClient

    from ai_ops.api import app
    from ai_ops.store import diag_repo as repo

    with TestClient(app) as client:
        monkeypatch.setattr(repo, "get_log", lambda i, table=None: None)
        assert client.get("/v1/diagnoses/123").status_code == 404


def test_api_escalate_existing_log_uses_ephemeral_preview(monkeypatch):
    """详情升级必须走临时预览，并保留原诊断快照里的采集参数。"""
    from fastapi.testclient import TestClient

    from ai_ops.api import app
    from ai_ops.store import diag_repo as repo

    monkeypatch.setattr(repo, "get_log", lambda i, table=None: {
        "id": i,
        "source": "dimple_violation_order",
        "error_text": "违规委托：合约 au",
        "business_date": "20261120",
        "error_code": 0,
        "key_json": json.dumps({"contractId": "au"}),
        "result_json": json.dumps({"rule_res": {"params": {"contract": "au"}}}),
    })
    seen = {}

    def fake_preview(rec):
        seen.update(rec)
        return {
            "text": rec["text"],
            "answer": {"root": "LLM 根因", "actions": [], "confidence": 0.8},
            "source": "LLM 诊断",
            "escalated": True,
        }

    def forbidden_manual_path(rec):
        raise AssertionError("详情升级不得调用会新增手工记录的 diagnose_escalated")

    with TestClient(app) as client:
        svc = app.state.service
        monkeypatch.setattr(svc, "escalation_allowed", lambda: True)
        monkeypatch.setattr(svc, "diagnose_escalated_ephemeral", fake_preview)
        monkeypatch.setattr(svc, "diagnose_escalated", forbidden_manual_path)
        response = client.post("/v1/diagnoses/7/escalate")

    assert response.status_code == 200
    assert response.json()["answer"]["root"] == "LLM 根因"
    assert seen["source"] == "dimple_violation_order"
    assert seen["key"] == {"contractId": "au"}
    assert seen["params"] == {"contract": "au"}


# ---------- M3 标注 ----------


def test_update_annotation(monkeypatch):
    calls = []
    monkeypatch.setattr(
        connection, "execute_write",
        lambda sql, params, table: calls.append((sql, params, table)))
    diag_repo.update_annotation(3, "wrong", "正确答案", "刘晓雨")
    sql, params, table = calls[0]
    assert "UPDATE" in sql
    assert params["annot_status"] == "wrong"
    assert params["annotator"] == "刘晓雨"
    assert params["log_id"] == 3


def test_api_annotation_200(monkeypatch):
    from fastapi.testclient import TestClient

    from ai_ops.api import app
    from ai_ops.store import diag_repo as repo

    with TestClient(app) as client:
        monkeypatch.setattr(repo, "get_log", lambda i, table=None: {"id": i})
        monkeypatch.setattr(repo, "update_annotation",
                            lambda *a, **k: 1)
        r = client.post("/v1/diagnoses/3/annotation", json={
            "annot_status": "correct",
            "correct_answer": None,
            "annotator": "刘晓雨",
        })
        assert r.status_code == 200
        assert r.json()["annotator"] == "刘晓雨"


def test_api_annotation_422_and_404(monkeypatch):
    from fastapi.testclient import TestClient

    from ai_ops.api import app
    from ai_ops.store import diag_repo as repo

    with TestClient(app) as client:
        # 非法标注状态
        r = client.post("/v1/diagnoses/3/annotation", json={
            "annot_status": "maybe", "annotator": "x"})
        assert r.status_code == 422
        # 标注人为空
        r2 = client.post("/v1/diagnoses/3/annotation", json={
            "annot_status": "correct", "annotator": "  "})
        assert r2.status_code == 422
        # 记录不存在
        monkeypatch.setattr(repo, "get_log", lambda i, table=None: None)
        r3 = client.post("/v1/diagnoses/3/annotation", json={
            "annot_status": "correct", "annotator": "刘晓雨"})
        assert r3.status_code == 404


def test_api_annotation_503(monkeypatch):
    from fastapi.testclient import TestClient

    from ai_ops.api import app
    from ai_ops.store import diag_repo as repo

    with TestClient(app) as client:
        def _boom(i, table=None):
            raise RuntimeError("table missing")

        monkeypatch.setattr(repo, "get_log", _boom)
        r = client.post("/v1/diagnoses/3/annotation", json={
            "annot_status": "correct", "annotator": "刘晓雨"})
        assert r.status_code == 503
