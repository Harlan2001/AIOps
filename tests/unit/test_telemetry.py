# -*- coding: utf-8 -*-
"""诊断链观测基线（3.1）：pipeline telemetry 各路径 + 聚合口径。"""
import pytest

from ai_ops import pipeline, telemetry


class _KB:
    def diagnose_card(self, text):
        return None


class _LLM:
    def __init__(self, ans=None):
        self.ans = ans

    def diagnose(self, ctx):
        return dict(self.ans) if self.ans is not None else None


def _run(rule_res, llm=None, force_llm=False, force_fast=False):
    eng = type("E", (), {"diagnose": lambda self, rec: rule_res})()
    return pipeline.diagnose({"text": "x", "ldate": "20250304", "errcode": 0,
                              "lsection": ""}, force_llm=force_llm,
                             force_fast=force_fast, eng=eng,
                             kbcli=_KB(), llm=llm or _LLM())


def _biz_nohit():
    return {"class": "biz", "verdict": "业务报错但未匹配规则，进入兜底 / 回流待补规则"}


def _biz_hit():
    return {"class": "biz", "type": {"id": "fund_short", "title": "策略资金不足"},
            "verdict": "诊断完成", "root": "策略资金不足", "action": ["补资金"]}


# ---------- pipeline telemetry 各路径 ----------

def test_telemetry_noise_ora():
    res = _run({"class": "noise", "verdict": "非故障提示，无需诊断"})
    assert res["telemetry"]["path"] == "noise_ora"
    assert res["telemetry"]["llm_called"] is False


def test_telemetry_rule_fast():
    res = _run(_biz_hit())
    assert res["telemetry"]["path"] == "rule_fast"
    assert res["telemetry"]["rule_hit"] is True
    assert res["telemetry"]["type_id"] == "fund_short"
    assert res["telemetry"]["llm_called"] is False


def test_telemetry_llm_no_type():
    res = _run(_biz_nohit(), llm=_LLM({"root": "llm 结论", "actions": []}))
    assert res["telemetry"]["path"] == "llm"
    assert res["telemetry"]["llm_called"] is True
    assert res["telemetry"]["fallback_reason"] == "no_type"
    assert res["source"].startswith("LLM")


def test_telemetry_llm_force():
    res = _run(_biz_hit(), llm=_LLM({"root": "llm 结论", "actions": []}),
               force_llm=True)
    assert res["telemetry"]["path"] == "llm"
    assert res["telemetry"]["fallback_reason"] == "force_llm"


def test_telemetry_fallback_hit_llm_down():
    # rule_hit 时正常流程走 rule_fast 不调 LLM；仅 force_llm 下 LLM 挂掉才回退规则
    res = _run(_biz_hit(), llm=_LLM(None), force_llm=True)
    assert res["telemetry"]["path"] == "fallback"
    assert res["telemetry"]["llm_called"] is True
    assert res["telemetry"]["fallback_reason"] == "llm_unavailable"
    assert res["telemetry"]["rule_hit"] is True
    assert res["source"].startswith("规则兜底")


def test_telemetry_fallback_nohit_llm_down():
    res = _run(_biz_nohit(), llm=_LLM(None))
    assert res["telemetry"]["path"] == "fallback"
    assert res["telemetry"]["fallback_reason"] == "llm_unavailable"
    assert res["telemetry"]["rule_hit"] is False


def test_telemetry_force_fast():
    res = _run(_biz_nohit(), force_fast=True)
    assert res["telemetry"]["path"] == "force_fast"
    assert res["telemetry"]["llm_called"] is False


# ---------- 聚合口径 ----------

def test_summarize_counts():
    results = [
        {"telemetry": {"path": "noise_ora", "llm_called": False}},
        {"telemetry": {"path": "rule_fast", "llm_called": False}},
        {"telemetry": {"path": "llm", "llm_called": True, "fallback_reason": "no_type"}},
        {"telemetry": {"path": "llm", "llm_called": True, "fallback_reason": "force_llm"}},
        {"telemetry": {"path": "fallback", "llm_called": True,
                       "fallback_reason": "llm_unavailable"}},
        {"telemetry": {"path": "force_fast", "llm_called": False}},
    ]
    s = telemetry.summarize(results)
    assert s["total"] == 6
    assert s["fast"] == 3
    assert s["llm_called"] == 3
    assert s["save_rate"] == pytest.approx(0.5)
    assert s["fallback_reasons"] == {"no_type": 1, "force_llm": 1, "llm_unavailable": 1}


def test_summarize_empty_and_missing_telemetry():
    assert telemetry.summarize([])["total"] == 0
    s = telemetry.summarize([{"no_telemetry": True}, {}])
    assert s["total"] == 2 and s["fast"] == 0 and s["llm_called"] == 0


def test_format_summary():
    s = telemetry.summarize([
        {"telemetry": {"path": "rule_fast", "llm_called": False}},
        {"telemetry": {"path": "llm", "llm_called": True, "fallback_reason": "no_type"}},
    ])
    line = telemetry.format_summary(s)
    assert "降本率 50.0%" in line and "no_type=1" in line
    assert telemetry.format_summary({"total": 0}) == "（无诊断记录，无观测数据）"
