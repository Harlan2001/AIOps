# -*- coding: utf-8 -*-
"""混合智能诊断管线（稳定契约层）：ML 分流/召回 + KB 知识卡 + 规则查库取证 + 决策门。

处理流程：
  1. ML 分流器：noise/ora/biz/other + 置信度（noise/ora 走快速路径，不调 LLM）
  2. ML 相似案例召回：为业务报错召回历史相似案例
  3. Dimple KB：按中文症状骨架检索领域知识卡（不可用则静默降级）
  4. 规则引擎：对已编码类型执行只读 SQL 诊断树，产出客观证据
  5. 决策门：
       高置信 + 规则命中   → 规则快速路径（毫秒、零 token）
       低置信/未覆盖/口语化 → 升级 LLM 诊断大脑
       LLM 未配置或调用失败 → 自动回退规则 / 兜底（离线可跑）

diagnose(record) -> dict 是未来 FastAPI / 调度器 / worker 唯一可依赖的调用面。
"""
from ai_ops import evidence
from ai_ops.engine import parser as P
from ai_ops.engine.rule_engine import Engine
from ai_ops.ml.router import Router
from ai_ops.ml.retriever import SimilarCaseIndex
from ai_ops.llm.client import LLMClient
from ai_ops.kb.client import KnowledgeClient


def _loc_str(loc):
    if not loc:
        return ""
    if loc.get("deep_pkg"):
        return "%s.%s:%s" % (loc["deep_pkg"], loc.get("deep_proc", ""), loc.get("deep_line", ""))
    return loc.get("module_label", "")


def diagnose(rec, force_llm=False, force_fast=False, llm=None, *,
             router=None, retriever=None, eng=None, kbcli=None):
    """对一条标准化记录执行混合诊断，返回结构化结果 dict。

    组件默认每次新建（脚本/CLI 用法）；服务化时可注入复用实例。
    llm 可注入 mock/定制客户端（测试与私有化 endpoint 桥接用）。
    """
    text = (rec.get("text") or "").strip()
    errcode = rec.get("errcode") or 0
    ldate = rec.get("ldate") or ""
    lsection = rec.get("lsection") or ""

    owns_eng = eng is None
    router = router or Router()
    retriever = retriever or SimilarCaseIndex.from_dataset()
    eng = eng or Engine()
    llm = llm or LLMClient()
    kbcli = kbcli or KnowledgeClient()

    try:
        rt = router.route(text, errcode)
        route = rt["route"]

        result = {"text": text, "errcode": errcode, "ldate": ldate,
                  "loc": _loc_str(P.parse_lsection(lsection)), "rt": rt,
                  "cases": [], "rule_res": None, "kb_card": None,
                  "answer": None, "source": ""}

        # ① ML 快速路径：噪音 / ORA，不查库、不调 LLM
        if route == "noise":
            result["source"] = "ML 快速路径"
            result["answer"] = {"root": "非故障提示（定时任务成功/无数据流水），无需诊断",
                                "actions": [], "confidence": rt["confidence"]}
            return result
        if route == "ora":
            result["source"] = "ML 快速路径"
            result["answer"] = {"root": "Oracle 技术错误（ORA/SQLCODE），建议转 DBA 处理",
                                "actions": ["转交 DBA 检查数据库执行计划、锁、约束等技术因素"],
                                "confidence": rt["confidence"]}
            return result

        # ② ML 召回相似案例（biz / other）
        cases = retriever.query(text, top_k=5)
        result["cases"] = cases

        # ②.5 领域知识层：按中文症状骨架检索 Dimple 知识库（机制/根因/处置手册）。
        #     用归一化后的中文症状检索，不用数字错误码（两套编码体系不一致）；
        #     知识库不可用时 diagnose_card 返回 None，静默降级，不影响主流程。
        result["kb_card"] = kbcli.diagnose_card(P.normalize_skeleton(text))

        # ③ 规则引擎只读查库取证
        rule_res = eng.diagnose(rec)
        result["rule_res"] = rule_res
        rule_hit = rule_res.get("verdict") == "诊断完成"

        # ④ 决策门：是否需要 LLM
        ml_high = bool(rt.get("biz_high")) and route == "biz"
        if force_fast:
            need_llm = False
        elif force_llm:
            need_llm = True
        else:
            # 高置信且规则命中 → 快速路径；否则（低置信/未覆盖/口语化）升级 LLM
            need_llm = not (rule_hit and ml_high)

        # ⑤ 最终诊断
        if need_llm:
            ctx = {
                "ldate": ldate, "errcode": errcode, "location": result["loc"],
                "text": text, "biz_type": rt.get("biz_type", "未知"),
                "params": rule_res.get("params") if rule_res else None,
                "cases": cases, "rule_res": rule_res,
                "kb_card": result["kb_card"],
                "kb_block": evidence.to_prompt_block(result["kb_card"]),
            }
            ans = llm.diagnose(ctx)
            if ans:
                ans.setdefault("confidence", 0.0)
                result["answer"] = ans
                result["source"] = "LLM 诊断大脑（ML 分流/召回 + 规则取证）"
                return result
            # LLM 不可用 → 回退
            if rule_hit:
                result["answer"] = {
                    "root": rule_res.get("root"),
                    "actions": rule_res.get("action", []),
                    "confidence": rt.get("biz_conf", 0.0),
                    "secondary": rule_res.get("secondary", [])}
                result["source"] = "规则兜底（LLM 未配置/不可用，已按规则查库）"
                return result
            result["answer"] = {
                "root": "未命中确定性规则，且 LLM 未配置；请人工介入或补充规则。"
                        "可参考下方 ML 召回的历史相似案例。",
                "actions": ["将该报错回流到开发侧，生成并审核新规则后发版"],
                "confidence": rt.get("biz_conf", 0.0)}
            result["source"] = "兜底（LLM 未配置 + 规则未覆盖）"
            return result

        # 规则快速路径
        result["answer"] = {
            "root": rule_res.get("root"),
            "actions": rule_res.get("action", []),
            "confidence": rt.get("biz_conf", 0.0),
            "secondary": rule_res.get("secondary", [])}
        result["source"] = "规则快速路径（ML 高置信 + 只读查库，零 token）"
        return result
    finally:
        if owns_eng:
            eng.close()
