# -*- coding: utf-8 -*-
"""诊断提示词构造：把报错、ML 召回的相似案例、规则查库证据组装成 LLM 输入。"""
import json

SYSTEM = (
    "你是 DIMPLE 期货/黄金交易清算系统（Oracle 数据库）的资深运维与 DBA 专家。"
    "用户会给你一条数据库业务报错、若干历史相似案例（机器学习检索得到），以及系统"
    "通过只读 SQL 查到的客观证据。请你：\n"
    "1. 只依据给定证据判断根因，证据中没有的数据一律不得编造，也不得臆测数据库被修改；\n"
    "2. 若证据不足以下结论，明确说明还需检查什么，不要硬下结论；\n"
    "3. 给出可执行的处置步骤（面向运维人员，具体到菜单/表/任务）。\n"
    "必须只输出一个 JSON 对象，不要输出多余文字，字段如下：\n"
    '{"root": "一句话根因（问题是什么）", '
    '"actions": ["处置步骤1", "处置步骤2"], '
    '"confidence": 0.0到1.0的置信度, '
    '"need_more_evidence": false, '
    '"evidence_note": "关键依据，引用查到的数据"}'
)


def _fmt_cases(cases):
    if not cases:
        return "（无）"
    lines = []
    for i, c in enumerate(cases, 1):
        lines.append(
            "%d. 历史模式：%s\n   历史出现 %d 次，最近 %s，错误码 %s，所属模块 %s\n   样例：%s"
            % (i, c["skeleton"], c["count"], c.get("last_date", ""),
               "/".join(c.get("errcodes", [])) or "-",
               "/".join(c.get("modules", [])) or "-", c["sample"]))
    return "\n".join(lines)


def _fmt_evidence(rule_res):
    if not rule_res:
        return "（系统未匹配到确定性查库规则，需你主要依据历史案例与报错语义判断）"
    lines = []
    for ev in rule_res.get("evidence", []):
        r = ev.get("r", {})
        if r.get("status") != "ok":
            lines.append("- %s：查询失败 %s" % (ev.get("title"), r.get("error", "")))
            continue
        if not r["rows"]:
            lines.append("- %s：无记录（0 行）" % ev.get("title"))
            continue
        cols = r["cols"]
        lines.append("- %s：%d 行" % (ev.get("title"), len(r["rows"])))
        for row in r["rows"][:3]:
            lines.append("    " + " | ".join(
                "%s=%s" % (c, row[k]) for k, c in enumerate(cols)))
    if rule_res.get("root"):
        lines.append("规则引擎的初步判断（供参考，请用证据校验）：%s" % rule_res["root"])
    return "\n".join(lines)


def build_messages(ctx):
    p = ctx.get("params", {}) or {}
    param_text = "，".join("%s=%s" % (k, v) for k, v in p.items()) or "（无）"
    user = (
        "【报错信息】\n"
        "时间：%s\n错误码：%s\n定位：%s\n"
        "报错文本：%s\nML 识别类型：%s\n抽取参数：%s\n\n"
        "【机器学习召回的历史相似案例】\n%s\n\n"
        "【系统只读 SQL 查库证据】\n%s\n\n"
        "请输出根因与处置 JSON。"
        % (
            ctx.get("ldate", ""),
            ctx.get("errcode", ""),
            ctx.get("location", ""),
            ctx.get("text", ""),
            ctx.get("biz_type", "未知"),
            param_text,
            _fmt_cases(ctx.get("cases")),
            _fmt_evidence(ctx.get("rule_res")),
        )
    )
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": user}]


def safe_parse_json(text):
    """从 LLM 输出中稳健提取 JSON（兼容 ```json 包裹）。"""
    if not text:
        return None
    t = text.strip()
    if "```" in t:
        # 取第一个代码块
        parts = t.split("```")
        for seg in parts:
            seg = seg.strip()
            if seg.startswith("json"):
                seg = seg[4:].strip()
            if seg.startswith("{"):
                t = seg
                break
    s, e = t.find("{"), t.rfind("}")
    if s >= 0 and e > s:
        try:
            return json.loads(t[s:e + 1])
        except Exception:
            return None
    return None
