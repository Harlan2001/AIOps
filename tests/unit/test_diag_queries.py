# -*- coding: utf-8 -*-
"""M2 历史诊断查询/聚合与 API 单元测试（离线打桩，不连真实 GaussDB）。"""
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
    fake.add("ORDER BY id", ["id", "source"], [[1, "ftr_err"], [2, None]])
    out = diag_repo.list_logs(source="ftr_err", offset=0, limit=10)
    assert out["total"] == 5
    assert len(out["items"]) == 2
    assert out["items"][0] == {"id": 1, "source": "ftr_err"}
    # 条件与分页参数被传入
    list_call = [c for c in fake.calls if "ORDER BY id" in c[0]][0]
    assert list_call[1]["source"] == "ftr_err"
    assert list_call[1]["limit"] == 10


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


def test_stats_zero_total(fake):
    fake.add("COUNT", ["cnt"], [[0]])
    out = diag_repo.stats()
    assert out["total"] == 0
    assert out["by_date"] == []
    assert out["abnormal_rate"] == 0.0


def test_stats_aggregation(fake):
    fake.add("COUNT", ["cnt"], [[10]])
    fake.add("GROUP BY business_date", ["grp", "cnt"],
             [["20250321", 6], ["20250320", 4]])
    fake.add("GROUP BY diag_type", ["grp", "cnt"], [["fund", 8]])
    fake.add("GROUP BY diag_class", ["grp", "cnt"], [["biz", 10]])
    fake.add("escalated = TRUE", ["cnt"], [[2]])
    fake.add("diag_status = 'error'", ["cnt"], [[1]])
    fake.add("annot_status IS NOT NULL", ["cnt"], [[3]])
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
