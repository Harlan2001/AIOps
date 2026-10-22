# -*- coding: utf-8 -*-
"""把诊断结果渲染成文本报告（纯模板，零模型）。"""


def render(res):
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
