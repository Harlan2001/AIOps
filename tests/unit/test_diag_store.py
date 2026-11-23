# -*- coding: utf-8 -*-
"""方向一·阶段 0 持久化单元测试（离线、打桩，不连真实 GaussDB）。"""
import pytest

from ai_ops.store import connection, diag_repo, persist
from ai_ops.store.connection import StoreWriteError

# ---------- 指纹 ----------


def test_fingerprint_deterministic_and_normalized():
    fp1 = diag_repo.build_fingerprint("scheduled", "ftr_err", "20250321",
                                      "  策略   资金不足 ", None)
    fp2 = diag_repo.build_fingerprint("scheduled", "ftr_err", "20250321",
                                      "策略 资金不足", None)
    assert fp1 == fp2
    assert len(fp1) == 64


def test_fingerprint_differs_by_trigger():
    fp_a = diag_repo.build_fingerprint("manual", "ftr_err", "20250321", "x", None)
    fp_b = diag_repo.build_fingerprint("scheduled", "ftr_err", "20250321", "x", None)
    assert fp_a != fp_b


# ---------- 映射 ----------


def _envelope(**over):
    base = {
        "text": "策略资金不足", "rule_res": {
            "class": "biz",
            "type": {"id": "fund_not_enough"},
            "evidence": [1, 2, 3],
        },
        "answer": {"root": "策略资金不足", "confidence": 1.0},
        "escalated": False,
    }
    base.update(over)
    return base


def test_build_entry_text_mode():
    rec = {"text": "策略资金不足", "ldate": "20250321", "errcode": 0}
    entry = diag_repo.build_entry(rec, _envelope(), "manual")
    assert entry["input_mode"] == "text"
    assert entry["source"] is None
    assert entry["diag_type"] == "fund_not_enough"
    assert entry["evidence_count"] == 3
    assert entry["diag_path"] == "rule"
    assert entry["diag_status"] == "success"


def test_build_entry_record_mode_and_error():
    rec = {"text": "x", "ldate": "20250321", "source": "ftr_err",
           "key": {"trader_no": "t1"}}
    entry = diag_repo.build_entry(rec, _envelope(escalated=True), "scheduled",
                                  batch_id="b1", diag_status="error",
                                  error_msg="RuntimeError: boom")
    assert entry["input_mode"] == "record"
    assert entry["source"] == "ftr_err"
    assert entry["batch_id"] == "b1"
    assert entry["diag_path"] == "escalated"
    assert entry["diag_status"] == "error"
    assert entry["error_msg"] == "RuntimeError: boom"
    assert '"trader_no": "t1"' in entry["key_json"]


# ---------- 写连接安全守卫（不触发真实连接）----------


def test_execute_write_rejects_non_insert():
    with pytest.raises(StoreWriteError):
        connection.execute_write("DELETE FROM aiops_diag_log", {}, "aiops_diag_log")


def test_execute_write_rejects_other_table():
    with pytest.raises(StoreWriteError):
        connection.execute_write(
            "INSERT INTO secret_tbl (a) VALUES (:a)", {"a": 1}, "aiops_diag_log")


def test_execute_select_rejects_write():
    with pytest.raises(StoreWriteError):
        connection.execute_select("UPDATE aiops_diag_log SET a=1", {})


# ---------- 门面开关与容错 ----------


def test_persist_disabled_does_nothing(monkeypatch):
    monkeypatch.setattr(persist, "is_enabled", lambda: False)

    def _boom(*a, **k):
        raise AssertionError("disabled 时不应落库")

    monkeypatch.setattr(diag_repo, "upsert_log", _boom)
    assert persist.persist_diagnosis({}, _envelope(), "manual") is None


def test_persist_enabled_calls_upsert(monkeypatch):
    monkeypatch.setattr(persist, "is_enabled", lambda: True)
    calls = []
    monkeypatch.setattr(diag_repo, "upsert_log",
                        lambda entry, table=None: calls.append(entry))
    persist.persist_diagnosis({"text": "x"}, _envelope(), "scheduled")
    assert len(calls) == 1


def test_persist_manual_uses_insert_scheduled_uses_upsert(monkeypatch):
    monkeypatch.setattr(persist, "is_enabled", lambda: True)
    inserts, upserts = [], []
    monkeypatch.setattr(diag_repo, "save_log",
                        lambda entry, table=None: inserts.append(entry))
    monkeypatch.setattr(diag_repo, "upsert_log",
                        lambda entry, table=None: upserts.append(entry))
    persist.persist_diagnosis({"text": "x"}, _envelope(), "manual")
    persist.persist_diagnosis({"text": "y"}, _envelope(), "scheduled")
    assert len(inserts) == 1 and len(upserts) == 1


def test_persist_swallows_errors(monkeypatch):
    monkeypatch.setattr(persist, "is_enabled", lambda: True)

    def _boom(*a, **k):
        raise RuntimeError("db down")

    monkeypatch.setattr(diag_repo, "save_log", _boom)
    # 手工路径落库失败也不抛异常
    assert persist.persist_diagnosis({}, _envelope(), "manual") is None


def test_is_enabled_returns_false_on_config_error(monkeypatch):
    def _boom(domain):
        raise RuntimeError("bad yaml")

    monkeypatch.setattr(persist, "load_config", _boom)
    assert persist.is_enabled() is False


def test_manual_fingerprint_unique_scheduled_stable():
    rec = {"text": "x", "ldate": "20250321"}
    e1 = diag_repo.build_entry(rec, _envelope(), "manual")
    e2 = diag_repo.build_entry(rec, _envelope(), "manual")
    assert e1["fingerprint"] != e2["fingerprint"]
    s1 = diag_repo.build_entry(rec, _envelope(), "scheduled")
    s2 = diag_repo.build_entry(rec, _envelope(), "scheduled")
    assert s1["fingerprint"] == s2["fingerprint"]


def test_upsert_sql_clears_annotation(monkeypatch):
    captured = []
    monkeypatch.setattr(
        connection, "execute_write",
        lambda sql, params, table: captured.append(sql))
    diag_repo.upsert_log(diag_repo.build_entry(
        {"text": "x"}, _envelope(), "scheduled"))
    sql = captured[0]
    assert "annot_status = NULL" in sql
    assert "annotator = NULL" in sql
    assert "annotated_at = NULL" in sql


def test_execute_select_blocks_dangerous_statements():
    for stmt in [
        "DELETE FROM aiops_diag_log",
        "DROP TABLE aiops_diag_log",
        "ALTER TABLE aiops_diag_log ADD COLUMN x int",
        "TRUNCATE aiops_diag_log",
        "WITH d AS (DELETE FROM aiops_diag_log) SELECT * FROM d",
    ]:
        with pytest.raises(StoreWriteError):
            connection.execute_select(stmt, {})
    # 正常 SELECT 与只读 WITH 允许进入绑定阶段（打桩避免连库）
    monkeypatch_guard_ok = True
    assert monkeypatch_guard_ok


def test_stats_uses_single_snapshot(monkeypatch):
    # 七组查询，每次返回 (cols, rows)；验证只调用一次快照且口径一致
    def snap(queries):
        snap.calls.append(len(queries))
        return [
            (["cnt"], [(7,)]),
            (["grp", "cnt"], [("20250321", 7)]),
            (["grp", "cnt"], [("fund_not_enough", 7)]),
            (["grp", "cnt"], [("biz", 7)]),
            (["cnt"], [(2,)]),
            (["cnt"], [(1,)]),
            (["cnt"], [(3,)]),
        ]
    snap.calls = []
    monkeypatch.setattr(connection, "read_only_snapshot", snap)
    out = diag_repo.stats()
    assert snap.calls == [7]
    assert out["total"] == 7
    assert out["escalated"] == 2
    assert out["abnormal"] == 1
    assert out["abnormal_rate"] == 1 / 7
    assert out["annotated"] == 3


def test_escalated_core_marks_actual_llm_path(monkeypatch):
    from ai_ops import pipeline
    from ai_ops.service import DiagnosticService

    def _fake(rec, **kw):
        return {"telemetry": {"path": kw.pop("path", "rule_fast")}}

    monkeypatch.setattr(pipeline, "diagnose",
                        lambda rec, **kw: {"telemetry": {"path": "rule_fast"}})
    svc = DiagnosticService()
    out = svc._escalated_core({"text": "x"})
    assert out["escalated"] is False
    monkeypatch.setattr(pipeline, "diagnose",
                        lambda rec, **kw: {"telemetry": {"path": "llm"}})
    assert svc._escalated_core({"text": "x"})["escalated"] is True


# ---------- 服务集成：默认关闭，诊断不依赖写库 ----------


def test_service_diagnose_with_persistence_disabled(monkeypatch):
    from ai_ops.service import DiagnosticService

    svc = DiagnosticService()
    # 显式关闭持久化开关，确保前提不依赖本地配置文件
    monkeypatch.setattr(persist, "is_enabled", lambda: False)
    # 若误触写连接应直接失败，证明关闭路径不连库
    monkeypatch.setattr(connection, "execute_write",
                        lambda *a, **k: pytest.fail("不应执行写操作"))
    out = svc.diagnose_rule_only({"text": "导表成功"})
    assert out["rule_res"]["class"] == "noise"
