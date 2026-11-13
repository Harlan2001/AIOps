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


def test_persist_swallows_errors(monkeypatch):
    monkeypatch.setattr(persist, "is_enabled", lambda: True)

    def _boom(*a, **k):
        raise RuntimeError("db down")

    monkeypatch.setattr(diag_repo, "upsert_log", _boom)
    # 不抛异常即通过
    assert persist.persist_diagnosis({}, _envelope(), "manual") is None


# ---------- 服务集成：默认关闭，诊断不依赖写库 ----------


def test_service_diagnose_with_persistence_disabled(monkeypatch):
    from ai_ops.service import DiagnosticService

    svc = DiagnosticService()
    # 若误触写连接应直接失败，证明关闭路径不连库
    monkeypatch.setattr(connection, "execute_write",
                        lambda *a, **k: pytest.fail("不应执行写操作"))
    out = svc.diagnose_rule_only({"text": "导表成功"})
    assert out["rule_res"]["class"] == "noise"
