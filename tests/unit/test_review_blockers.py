# -*- coding: utf-8 -*-
"""评审合并阻断项 B1–B10 的回归测试（本文件与修复同 PR 提交）。

原则：全部用 FakeDB/monkeypatch 隔离真实 GaussDB，离线可跑、确定性。
"""
import pytest

from ai_ops.engine import error_records as ER
from ai_ops.engine.db import DatabaseUnavailable
from ai_ops.engine.rule_engine import Engine
from ai_ops.service import MAX_BATCH, DiagnosticService


# ---------- 通用 FakeDB ----------


class FakeDB:
    """按 SQL 子串返回预置 (cols, rows)；未命中返回空结果。"""

    def __init__(self):
        self.routes = []
        self.calls = []

    def add(self, key, cols, rows):
        self.routes.append((key, list(cols), [list(r) for r in rows]))

    def __call__(self, sql, params=None, limit=None):
        self.calls.append((sql, params))
        for key, cols, rows in self.routes:
            if key in sql:
                return cols, rows
        return ["dummy"], []


@pytest.fixture
def eng(monkeypatch):
    e = Engine()
    fake = FakeDB()
    monkeypatch.setattr(ER, "query", fake)
    monkeypatch.setattr("ai_ops.engine.rule_engine.query", fake)
    e._fake = fake
    yield e
    e.close()


# ---------- B1：alarm 当日表列 + SOURCES 纳入 977 清单校验 ----------


def test_b1_alarm_today_uses_alarm_time_and_two_col_key():
    src = ER.SOURCES["alarm"]
    assert ER.date_col_of(src, history=False) == "alarm_time"
    assert ER.key_cols_of(src, history=False) == ["seq_no", "alarm_type"]
    # 历史表保持原定义
    assert ER.date_col_of(src, history=True) == "alarm_date"
    assert ER.key_cols_of(src, history=True) == ["alarm_date", "seq_no", "alarm_type"]


def test_b1_all_source_tables_and_columns_exist_in_catalog():
    """每个来源（含当日表）引用的表/列都必须在 977 清单内——B1 类问题应被本测试拦下。"""
    from ai_ops.engine import schema_check as SC
    tables = SC.load_catalog()
    assert len(tables) > 900
    for sid, src in ER.SOURCES.items():
        for history in (True, False):
            tbl = src.his if history else (src.today or src.his)
            assert tbl in tables, "%s 引用清单外表 %s" % (sid, tbl)
            missing = set(ER._all_cols(src, history)) - tables[tbl]
            assert not missing, "%s 表 %s 引用清单外列 %s" % (sid, tbl, missing)


# ---------- B2：主键缺失/非主键显式报错；db._bind 拒绝 None；CLI 有 --exch ----------


def test_b2_get_record_missing_key_raises(monkeypatch):
    monkeypatch.setattr(ER, "query", FakeDB())
    with pytest.raises(ER.RecordKeyError, match="缺少必需主键列"):
        ER.get_record("ftr_err", {"trade_date": "20250101", "trader_no": "t1"})


def test_b2_get_record_unknown_key_raises(monkeypatch):
    monkeypatch.setattr(ER, "query", FakeDB())
    key = {"trade_date": "20250101", "trader_no": "t1",
           "local_no": "l1", "purpose_code": "ZY", "client_id": "c1"}
    with pytest.raises(ER.RecordKeyError, match="非主键参数"):
        ER.get_record("ftr_err", key)


def test_b2_db_bind_rejects_none():
    from ai_ops.engine.db import _bind
    with pytest.raises(ValueError, match="绑定参数缺失"):
        _bind("SELECT * FROM dimple.t WHERE a = :a AND b = :b", {"a": 1})


def test_b2_cli_has_exch_arg():
    from ai_ops.cli import _build_parser
    args = _build_parser().parse_args(
        ["--source", "flow_control", "--date", "20250101",
         "--flow-code", "001", "--exch", "01"])
    assert args.exch == "01"


# ---------- B3：flow runbook 主检查不再恒真、不再依赖 flow_code ----------


def test_b3_runbook_primary_sql_filters_oper_result_without_flow_code():
    from ai_ops import rules_store
    for name in ("rb_margin_mismatch", "rb_settle_not_ready"):
        rb = rules_store.load_runbook(name)
        primary = next(s for s in rb["steps"] if s.get("primary"))
        sql = primary["sql"].lower()
        assert "oper_result = '0'" in sql
        assert ":flow_code" not in sql


def test_b3_primary_empty_rows_triggers_on_fail(eng):
    """补 exch 后主检查实际执行；0 行（无失败步骤）→ exists(false) != want(true) → on_fail。"""
    rec = {"text": "[交易所=>01]对账不平", "ldate": "20250101", "errcode": 0}
    res = eng.diagnose(rec)
    assert res["primary_evidence_ok"] is True
    assert "未发现对账不成功" in res["root"]


def test_b3_primary_hit_row_uses_default_conclusion(eng):
    flow_cols = ["clear_date", "flow_code", "exch_code", "oper_name",
                 "oper_flag", "oper_result", "oper_time", "err_msg"]
    eng._fake.add("tc_his_flow_control", flow_cols,
                  [["20250101", "001", "01", "保证金对账", "1", "0", "09000000", "不平"]])
    rec = {"text": "[交易所=>01]对账不平", "ldate": "20250101", "errcode": 0}
    res = eng.diagnose(rec)
    assert "准备金/保证金对账不平" in res["root"]


# ---------- B4：missing_params 结构化 ----------


def test_b4_missing_params_structured(eng):
    res = eng.diagnose({"text": "对账不平", "ldate": "20250101", "errcode": 0})
    assert res.get("missing_params")
    entry = res["missing_params"][0]
    assert entry["step"] == "settlement_status"
    assert "exch" in entry["missing"]


# ---------- B8：证据可信度标记（引擎层） ----------


def test_b8_engine_flags_missing_vs_success(eng):
    res_missing = eng.diagnose(
        {"text": "对账不平", "ldate": "20250101", "errcode": 0})
    assert res_missing["primary_evidence_ok"] is False
    assert res_missing["evidence_complete"] is False

    flow_cols = ["clear_date", "flow_code", "exch_code", "oper_name",
                 "oper_flag", "oper_result", "oper_time", "err_msg"]
    eng._fake.add("tc_his_flow_control", flow_cols,
                  [["20250101", "001", "01", "x", "1", "0", "09000000", ""]])
    res_ok = eng.diagnose(
        {"text": "[交易所=>01]对账不平", "ldate": "20250101", "errcode": 0})
    assert res_ok["primary_evidence_ok"] is True
    assert res_ok["evidence_complete"] is True


# ---------- B8：pipeline 降置信度 + evidence_note ----------


def test_b8_pipeline_degraded_confidence(eng):
    from ai_ops.pipeline import diagnose
    res = diagnose(
        {"text": "对账不平", "ldate": "20250101", "errcode": 0},
        eng=eng, llm=_UnavailableLLM())
    assert res["answer"]["confidence"] == 0.4
    assert res["answer"].get("evidence_note")
    assert "降置信度" in res["source"]


def test_b8_pipeline_full_confidence_with_evidence(eng):
    flow_cols = ["clear_date", "flow_code", "exch_code", "oper_name",
                 "oper_flag", "oper_result", "oper_time", "err_msg"]
    eng._fake.add("tc_his_flow_control", flow_cols,
                  [["20250101", "001", "01", "x", "1", "0", "09000000", ""]])
    from ai_ops.pipeline import diagnose
    res = diagnose(
        {"text": "[交易所=>01]对账不平", "ldate": "20250101", "errcode": 0},
        eng=eng, llm=_UnavailableLLM())
    assert res["answer"]["confidence"] == 1.0


class _UnavailableLLM:
    def available(self):
        return False

    def diagnose(self, ctx):
        return None


# ---------- B9：doctor 不再检查 numpy ----------


def test_b9_doctor_has_no_numpy():
    from ai_ops.ops import doctor
    pkgs = [d for _m, d in doctor._PKGS]
    assert "numpy" not in pkgs


# ---------- B10：自成交子串平分路由 ----------


@pytest.mark.parametrize("text,expect_id", [
    ("自成交预警，触发阀值", "self_trade_alert"),
    ("自成交次数达到预警阀值", "self_trade_alert"),
    ("自成交风险，请检查", "self_trade"),
    ("自成交禁止", "self_trade"),
    ("触发自成交", "self_trade"),
])
def test_b10_self_trade_tie_routing(eng, text, expect_id):
    t, _score = eng.match_type(text, 0)
    assert t["id"] == expect_id


# ---------- API 层 B5/B6/B7（FastAPI TestClient） ----------


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from ai_ops.api import app
    with TestClient(app) as c:
        yield c


def test_b5_unknown_source_records_404(client):
    r = client.get("/v1/records", params={"source": "nope", "date": "20250101"})
    assert r.status_code == 404
    assert "未知错误来源" in r.json()["detail"]


def test_b5_unknown_source_batch_404(client):
    r = client.post("/v1/batch-diagnose",
                    json={"source": "nope", "date": "20250101"})
    assert r.status_code == 404


def test_b6_record_mode_db_unavailable_503(client, monkeypatch):
    def boom(self, source, key):
        raise DatabaseUnavailable("连接超时")
    monkeypatch.setattr(DiagnosticService, "get_record", boom)
    r = client.post("/v1/diagnose", json={
        "record": {"source": "ftr_err", "date": "20250101",
                   "key": {"trader_no": "t1", "local_no": "l1", "purpose_code": "ZY"}}})
    assert r.status_code == 503


def test_b6_records_db_unavailable_503(client, monkeypatch):
    def boom(self, source, date, limit=None):
        raise DatabaseUnavailable("连接超时")
    monkeypatch.setattr(DiagnosticService, "list_records", boom)
    r = client.get("/v1/records", params={"source": "ftr_err", "date": "20250101"})
    assert r.status_code == 503


def test_b7_batch_isolated_per_item_error_and_truncation(client, monkeypatch):
    fake_recs = [
        {"text": "报错%d" % i, "ldate": "20250101", "source": "ftr_err",
         "errcode": 0, "key": {"i": i}} for i in range(MAX_BATCH + 5)]

    def fake_list(self, source, date, limit=None):
        return fake_recs[:limit]

    def fake_diagnose(self, rec):
        if rec["key"]["i"] == 2:
            raise RuntimeError("单条炸了")
        return {"class": "biz", "verdict": "诊断完成", "root": "ok", "action": []}

    monkeypatch.setattr(DiagnosticService, "list_records", fake_list)
    monkeypatch.setattr(Engine, "diagnose", fake_diagnose)

    r = client.post("/v1/batch-diagnose",
                    json={"source": "ftr_err", "date": "20250101"})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == MAX_BATCH
    assert body["truncated"] is True
    assert body["results"][2].get("error") == "RuntimeError: 单条炸了"
    assert body["results"][0]["result"]["root"] == "ok"


def test_b7_records_endpoint_limit_capped(client, monkeypatch):
    def fake_list(self, source, date, limit=None):
        assert limit <= MAX_BATCH
        return [{"text": "x", "errcode": 0} for _ in range(limit)]
    monkeypatch.setattr(DiagnosticService, "list_records", fake_list)
    r = client.get("/v1/records",
                   params={"source": "ftr_err", "date": "20250101", "limit": 99999})
    assert r.status_code == 200
    assert r.json()["count"] == MAX_BATCH
