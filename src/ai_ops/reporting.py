# -*- coding: utf-8 -*-
"""诊断结果文本渲染（纯模板，零模型/零 IO）：混合管线报告 + 纯规则报告。"""
from ai_ops import evidence

W = 96


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


def render_hybrid(res):
    """混合管线 diagnose() 结果 -> CLI 文本报告。"""
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

    kb_card = res.get("kb_card")
    if kb_card:
        L.append("【领域知识卡（Dimple 知识库 · 机制/根因/处置）】")
        L += evidence.to_report_lines(kb_card)

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


def render_rule(res):
    """规则引擎 Engine.diagnose() 结果 -> 纯规则文本报告。"""
    L = []
    L.append("=" * 92)
    L.append("【TLOG 业务报错诊断报告】")
    L.append("=" * 92)

    loc = res.get("loc") or {}
    if res.get("ldate"):
        L.append("报错时间 : %s" % res["ldate"])
    if res.get("errcode"):
        L.append("错误码   : %s" % res["errcode"])
    if loc.get("deep_pkg"):
        L.append("报错位置 : %s . %s : %s" % (
            loc.get("deep_pkg"), loc.get("deep_proc"), loc.get("deep_line")))
    L.append("报错文本 : %s" % res["text"])

    cls = res.get("class")
    if cls in ("noise", "ora", "other") or "type" not in res:
        L.append("-" * 92)
        L.append("判定     : %s" % res.get("verdict"))
        L.append("=" * 92)
        return "\n".join(L)

    t = res["type"]
    L.append("-" * 92)
    L.append("问题类型 : %s（%s）" % (t.get("title"), t.get("id")))
    p = res.get("params") or {}
    shown = {k: v for k, v in p.items() if v not in (None, "") and k != "trade_date"}
    if shown:
        L.append("报错参数 : " + "，".join("%s=%s" % (k, v) for k, v in shown.items()))
    L.append("诊断日期 : %s" % p.get("trade_date"))

    L.append("-" * 92)
    L.append("【排查证据】")
    for ev in res.get("evidence", []):
        r = ev["r"]
        if r["status"] == "missing_params":
            L.append("  - %s：缺少参数 %s，跳过" % (ev["title"], ",".join(r["missing"])))
            continue
        n = len(r["rows"])
        L.append("  - %s：%d 行" % (ev["title"], n))
        if r["rows"]:
            L.append("      列: %s" % " | ".join(r["cols"]))
            for row in r["rows"][:3]:
                L.append("      %s" % " | ".join(str(x) for x in row))

    L.append("-" * 92)
    L.append("【问题是什么】")
    L.append("  " + res.get("root", ""))
    for s in res.get("secondary", []):
        L.append("  附带发现（%s）：%s" % (s.get("title"), s.get("root")))
    L.append("【怎么解决】")
    for i, a in enumerate(res.get("action", []), 1):
        L.append("  %d. %s" % (i, a))
    for s in res.get("secondary", []):
        L.append("  —— 针对【%s】" % s.get("title"))
        for a in s.get("action", []):
            L.append("     · %s" % a)
    L.append("=" * 92)
    return "\n".join(L)
