# -*- coding: utf-8 -*-
"""诊断管线（稳定契约层）：规则引擎分流与查库取证 + KB 知识卡 + 决策门。

处理流程（无 ML，分流与类型识别由规则引擎确定性完成）：
  1. 规则引擎 Engine.diagnose：噪音/技术错误/业务分类 + 20 类型识别 + 只读 SQL 查库取证
  2. Dimple KB：按中文症状骨架检索领域知识卡（不可用则静默降级）
  3. 决策门：
       噪音/技术错误 → 规则快速路径（零 token，不调 LLM）
       规则命中     → 规则快速路径（只读查库取证，零 token）
       规则未覆盖/口语化 → 升级 LLM 诊断大脑
       LLM 未配置或调用失败 → 自动回退规则 / 兜底（离线可跑）

diagnose(record) -> dict 是未来 FastAPI / 调度器 / worker 唯一可依赖的调用面。
"""
from ai_ops import evidence
from ai_ops.engine import parser as P
from ai_ops.engine.rule_engine import Engine
from ai_ops.llm.client import LLMClient
from ai_ops.kb.client import KnowledgeClient


def _loc_str(loc):
    if not loc:
        return ""
    if loc.get("deep_pkg"):
        return "%s.%s:%s" % (loc["deep_pkg"], loc.get("deep_proc", ""), loc.get("deep_line", ""))
    return loc.get("module_label", "")


# 主检查无成功取证时的降级置信度（结论仍可参考，但必须显式标注证据不完整）
LOW_CONFIDENCE = 0.4


def _evidence_note(rule_res):
    """汇总缺参/执行失败的取证步骤，生成显式降级说明（B8：缺证不能再静默给满分）。"""
    parts = []
    mp = rule_res.get("missing_params") or []
    if mp:
        names = "、".join(
            "%s（缺 %s）" % (x.get("step"), "/".join(x.get("missing", []))) for x in mp)
        parts.append("以下取证步骤缺参未执行：%s" % names)
    se = rule_res.get("sql_errors") or []
    if se:
        names = "、".join(
            "%s（%s）" % (x.get("step"), str(x.get("error", ""))[:60]) for x in se)
        parts.append("以下取证步骤执行失败：%s" % names)
    return "；".join(parts)


def _rule_answer(rule_res, confidence):
    """从规则引擎结果构造 answer；证据不完整时附 evidence_note。"""
    ans = {
        "root": rule_res.get("root"),
        "actions": rule_res.get("action", []),
        "confidence": confidence,
        "secondary": rule_res.get("secondary", []),
    }
    note = _evidence_note(rule_res)
    if note:
        ans["evidence_note"] = note
    return ans


def _mk_telemetry(path, llm_called=False, fallback_reason=None, rule_hit=False,
                  cls=None, type_id=None):
    """诊断链观测（3.1 观测基线）：记录本条走了哪条路径、是否调 LLM、兜底原因。"""
    return {"path": path, "llm_called": llm_called,
            "fallback_reason": fallback_reason, "rule_hit": rule_hit,
            "cls": cls, "type_id": type_id}


def diagnose(rec, force_llm=False, force_fast=False, llm=None, *,
             eng=None, kbcli=None):
    """对一条标准化记录执行规则 + 知识库 + LLM 混合诊断，返回结构化结果 dict。

    组件默认每次新建（脚本/CLI 用法）；服务化时可注入复用实例。
    llm 可注入 mock/定制客户端（测试与私有化 endpoint 桥接用）。
    """
    text = (rec.get("text") or "").strip()
    errcode = rec.get("errcode") or 0
    ldate = rec.get("ldate") or ""
    lsection = rec.get("lsection") or ""

    owns_eng = eng is None
    eng = eng or Engine()
    llm = llm or LLMClient()
    kbcli = kbcli or KnowledgeClient()

    try:
        # 规则引擎：分流（噪音/技术错误/业务/other）+ 类型识别 + 只读 SQL 查库取证
        rule_res = eng.diagnose(rec)
        cls = rule_res.get("class")
        # B8：rule_hit 必须有成功取证的主检查；verdict 完成但主检查全缺证/失败仅算降级
        verdict_done = rule_res.get("verdict") == "诊断完成"
        primary_ok = bool(rule_res.get("primary_evidence_ok"))
        rule_hit = verdict_done and primary_ok
        degraded = verdict_done and not primary_ok
        confidence = 1.0 if rule_hit else LOW_CONFIDENCE
        type_id = (rule_res.get("type") or {}).get("id")

        result = {"text": text, "errcode": errcode, "ldate": ldate,
                  "loc": _loc_str(P.parse_lsection(lsection)),
                  "rule_res": rule_res, "kb_card": None,
                  "answer": None, "source": "", "telemetry": None}

        # ① 规则快速路径：噪音 / 技术错误（引擎直接判定，不查库、不调 LLM）
        if cls in ("noise", "ora"):
            result["answer"] = {"root": rule_res.get("verdict"),
                                "actions": [], "confidence": 1.0}
            result["source"] = "规则快速路径（噪音/技术错误，零 token）"
            result["telemetry"] = _mk_telemetry("noise_ora", cls=cls)
            return result

        # ② 领域知识层：按归一化中文症状检索 Dimple 知识库（不可用静默降级）
        result["kb_card"] = kbcli.diagnose_card(P.normalize_skeleton(text))

        # ③ 规则命中 → 快速路径（零 token）；证据不完整时仍走零 token 但降置信度并标注
        if (rule_hit or degraded) and not force_llm:
            result["answer"] = _rule_answer(rule_res, confidence)
            if rule_hit:
                result["source"] = "规则快速路径（规则查库取证，零 token）"
                result["telemetry"] = _mk_telemetry("rule_fast", rule_hit=True,
                                                    cls=cls, type_id=type_id)
            else:
                result["source"] = "规则快速路径（主检查无成功取证，已降置信度，零 token）"
                result["telemetry"] = _mk_telemetry(
                    "rule_fast", rule_hit=False,
                    fallback_reason="insufficient_evidence", cls=cls, type_id=type_id)
            return result

        if force_fast:
            # 强制快速：规则未命中也按规则结果返回，置信度同样与证据挂钩
            result["answer"] = _rule_answer(rule_res, confidence)
            result["answer"]["root"] = (
                rule_res.get("root") or rule_res.get("verdict", ""))
            result["source"] = "规则快速路径（force_fast）"
            result["telemetry"] = _mk_telemetry("force_fast", cls=cls)
            return result

        # ④ LLM 兜底（规则未覆盖 / 口语化长尾 / 显式要求升级）
        ctx = {
            "ldate": ldate, "errcode": errcode, "location": result["loc"],
            "text": text,
            "biz_type": (rule_res.get("type") or {}).get("title", "未知"),
            "params": rule_res.get("params") if rule_res else None,
            "rule_res": rule_res,
            "kb_card": result["kb_card"],
            "kb_block": evidence.to_prompt_block(result["kb_card"]),
        }
        ans = llm.diagnose(ctx)
        if ans:
            ans.setdefault("confidence", 0.0)
            result["answer"] = ans
            result["source"] = "LLM 诊断大脑（规则识别 + KB 知识卡 + 规则取证）"
            result["telemetry"] = _mk_telemetry(
                "llm", llm_called=True,
                fallback_reason="force_llm" if force_llm else "no_type",
                rule_hit=rule_hit, cls=cls, type_id=type_id)
            return result
        # LLM 不可用 → 回退：有规则结论（含降级）按规则返回，否则通用兜底
        if rule_hit or degraded:
            result["answer"] = _rule_answer(rule_res, confidence)
            result["source"] = "规则兜底（LLM 未配置/不可用，已按规则查库）"
            result["telemetry"] = _mk_telemetry(
                "fallback", llm_called=True, fallback_reason="llm_unavailable",
                rule_hit=rule_hit, cls=cls, type_id=type_id)
            return result
        result["answer"] = {
            "root": "未命中确定性规则，且 LLM 未配置；请人工介入或补充规则。",
            "actions": ["将该报错回流到开发侧，生成并审核新规则后发版"],
            "confidence": 0.0}
        result["source"] = "兜底（LLM 未配置 + 规则未覆盖）"
        result["telemetry"] = _mk_telemetry(
            "fallback", llm_called=True, fallback_reason="llm_unavailable",
            rule_hit=False, cls=cls)
        return result
    finally:
        if owns_eng:
            eng.close()
