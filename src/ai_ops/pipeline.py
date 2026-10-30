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
        rule_hit = rule_res.get("verdict") == "诊断完成"

        result = {"text": text, "errcode": errcode, "ldate": ldate,
                  "loc": _loc_str(P.parse_lsection(lsection)),
                  "rule_res": rule_res, "kb_card": None,
                  "answer": None, "source": ""}

        # ① 规则快速路径：噪音 / 技术错误（引擎直接判定，不查库、不调 LLM）
        if cls in ("noise", "ora"):
            result["answer"] = {"root": rule_res.get("verdict"),
                                "actions": [], "confidence": 1.0}
            result["source"] = "规则快速路径（噪音/技术错误，零 token）"
            return result

        # ② 领域知识层：按归一化中文症状检索 Dimple 知识库（不可用静默降级）
        result["kb_card"] = kbcli.diagnose_card(P.normalize_skeleton(text))

        # ③ 规则命中 → 快速路径（零 token）；否则升级 LLM
        if rule_hit and not force_llm:
            result["answer"] = {
                "root": rule_res.get("root"),
                "actions": rule_res.get("action", []),
                "confidence": 1.0,
                "secondary": rule_res.get("secondary", [])}
            result["source"] = "规则快速路径（规则查库取证，零 token）"
            return result

        if force_fast:
            # 强制快速：规则未命中也按规则结果返回
            result["answer"] = {
                "root": rule_res.get("root") or rule_res.get("verdict", ""),
                "actions": rule_res.get("action", []),
                "confidence": 1.0}
            result["source"] = "规则快速路径（force_fast）"
            return result

        # ④ LLM 兜底（规则未覆盖 / 口语化长尾）
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
            return result
        # LLM 不可用 → 回退
        if rule_hit:
            result["answer"] = {
                "root": rule_res.get("root"),
                "actions": rule_res.get("action", []),
                "confidence": 1.0,
                "secondary": rule_res.get("secondary", [])}
            result["source"] = "规则兜底（LLM 未配置/不可用，已按规则查库）"
            return result
        result["answer"] = {
            "root": "未命中确定性规则，且 LLM 未配置；请人工介入或补充规则。",
            "actions": ["将该报错回流到开发侧，生成并审核新规则后发版"],
            "confidence": 0.0}
        result["source"] = "兜底（LLM 未配置 + 规则未覆盖）"
        return result
    finally:
        if owns_eng:
            eng.close()
