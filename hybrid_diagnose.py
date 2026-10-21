# -*- coding: utf-8 -*-
"""混合智能诊断管线（LLM 为主 + ML 前置/召回 + 规则查库取证）。

处理流程：
  1. ML 分流器：noise/ora/biz/other + 置信度（noise/ora 走快速路径，不调 LLM）
  2. ML 相似案例召回：为业务报错召回历史相似案例
  3. 规则引擎：对已编码类型执行只读 SQL 诊断树，产出客观证据
  4. 决策门：
       高置信 + 规则命中         → 规则快速路径（毫秒、零 token）
       低置信 / 规则未覆盖 / 口语化 → 升级 LLM 诊断大脑
       LLM 未配置或调用失败       → 自动回退规则 / 兜底（离线可跑）
  5. 输出结构化报告，并标注每一步由谁完成（可解释、可审计）。

用法:
    python hybrid_diagnose.py --id 4811525544
    python hybrid_diagnose.py --text "[合约=>Au9999]结算价不存在"
    python hybrid_diagnose.py --id xxx --llm      # 强制走 LLM
    python hybrid_diagnose.py --id xxx --fast     # 强制规则快速路径（不调 LLM）
"""
import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from diagnose import get_record_by_id              # noqa: E402
from engine import parser as P                     # noqa: E402
from engine.rule_engine import Engine             # noqa: E402
from ml.router import Router                       # noqa: E402
from ml.retriever import SimilarCaseIndex         # noqa: E402
from llm.client import LLMClient                  # noqa: E402

W = 96


def _loc_str(loc):
    if not loc:
        return ""
    if loc.get("deep_pkg"):
        return "%s.%s:%s" % (loc["deep_pkg"], loc.get("deep_proc", ""), loc.get("deep_line", ""))
    return loc.get("module_label", "")


def _fmt_evidence(rule_res):
    out = []
    if not rule_res:
        return out
    for ev in rule_res.get("evidence", []):
        r = ev.get("r", {})
        if r.get("status") != "ok":
            out.append("  - %s：跳过（%s）" % (ev.get("title"), r.get("missing", "查询失败")))
            continue
        if not r["rows"]:
            out.append("  - %s：无记录（0 行）" % ev.get("title"))
            continue
        out.append("  - %s：%d 行" % (ev.get("title"), len(r["rows"])))
        for row in r["rows"][:2]:
            out.append("      " + " | ".join("%s=%s" % (c, v) for c, v in zip(r["cols"], row)))
    return out


def diagnose(rec, force_llm=False, force_fast=False, llm=None):
    text = (rec.get("text") or "").strip()
    errcode = rec.get("errcode") or 0
    ldate = rec.get("ldate") or ""
    lsection = rec.get("lsection") or ""

    router = Router()
    retriever = SimilarCaseIndex.from_dataset()
    eng = Engine()
    llm = llm or LLMClient()

    try:
        rt = router.route(text, errcode)
        route = rt["route"]

        result = {"text": text, "errcode": errcode, "ldate": ldate,
                  "loc": _loc_str(P.parse_lsection(lsection)), "rt": rt,
                  "cases": [], "rule_res": None, "answer": None, "source": ""}

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
        eng.close()


def render(res):
    L = ["=" * W, "【TLOG 智能诊断报告 · ML 分流 + 规则取证 + LLM 大脑】", "=" * W]
    L.append("报错时间 : %s" % res["ldate"])
    L.append("错误码   : %s" % res["errcode"])
    if res["loc"]:
        L.append("报错位置 : %s" % res["loc"])
    L.append("报错文本 : %s" % res["text"][:200])
    rt = res["rt"]
    L.append("-" * W)
    L.append("【ML 分流】路由=%s 置信度=%.3f" % (rt["route"], rt["confidence"]))
    if rt.get("biz_type"):
        L.append("    业务类型=%s 类型置信度=%.3f %s"
                 % (rt["biz_type"], rt.get("biz_conf", 0.0),
                    "（高置信）" if rt.get("biz_high") else "（低置信→升级 LLM）"))

    cases = res.get("cases", [])
    if cases:
        L.append("【ML 相似案例召回】")
        for c in cases:
            L.append("  · %.3f | %s 次 | 最近 %s | 码 %s"
                     % (c["similarity"], c["count"], c["last_date"],
                        "/".join(c["errcodes"]) or "-"))
            L.append("           %s" % c["skeleton"][:80])

    ev = _fmt_evidence(res.get("rule_res"))
    if ev:
        L.append("【只读 SQL 查库证据（规则引擎）】")
        L += ev

    a = res["answer"] or {}
    L.append("-" * W)
    L.append("【最终诊断】来源：%s" % res["source"])
    L.append("  问题是什么：%s" % a.get("root", ""))
    if a.get("evidence_note"):
        L.append("  依据：%s" % a["evidence_note"])
    for s in a.get("secondary", []):
        L.append("  附带发现（%s）：%s" % (s.get("title"), s.get("root")))
    L.append("  怎么解决：")
    for i, act in enumerate(a.get("actions", []), 1):
        L.append("    %d. %s" % (i, act))
    if a.get("confidence") is not None:
        L.append("  诊断置信度：%.3f" % float(a.get("confidence", 0)))
    L.append("=" * W)
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id")
    ap.add_argument("--text")
    ap.add_argument("--ldate", default="")
    ap.add_argument("--errcode", type=int, default=0)
    ap.add_argument("--llm", action="store_true", help="强制走 LLM")
    ap.add_argument("--fast", action="store_true", help="强制规则快速路径")
    args = ap.parse_args()

    if args.id:
        rec = get_record_by_id(int(args.id))
        if not rec:
            print("未找到 ID=%s 的日志" % args.id)
            sys.exit(1)
    elif args.text:
        rec = {"text": args.text, "ldate": args.ldate, "errcode": args.errcode,
               "lsection": "", "func_no": None}
    else:
        ap.print_help()
        sys.exit(2)

    res = diagnose(rec, force_llm=args.llm, force_fast=args.fast)
    print(render(res))


if __name__ == "__main__":
    main()
