# -*- coding: utf-8 -*-
"""诊断提示词构造：把报错、ML 召回的相似案例、领域知识卡、规则查库证据组装成 LLM 输入。"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kb.client import KnowledgeClient  # noqa: E402

SYSTEM = (
    "你是 DIMPLE 期货/黄金交易清算系统（Oracle 数据库）的资深运维与 DBA 专家。"
    "用户会给你一条数据库业务报错，并提供三类证据：\n"
    "① 机器学习召回的历史相似案例：这种报错以前发生过多少次、长什么样（先验）；\n"
    "② Dimple 官方知识库的领域诊断卡：候选根因分支、成立/反证条件、只读 SQL、日志锚点、"
    "处置的允许/禁止条件、副作用、恢复验证与回退边界（机制与手册）；\n"
    "③ 系统通过只读 SQL 实际查到的库内客观证据（现场事实）。\n"
    "请你：\n"
    "1. 只依据三类证据判断根因，证据中没有的数据一律不得编造，也不得臆测数据库被修改；\n"
    "2. 以③现场查库事实为准，用它验证或排除②知识库列出的候选分支；知识库是冻结源码取证、"
    "未现场核实，其中只读 SQL 未在现场执行，不得声称已执行、不得据此臆测现场状态；\n"
    "3. 若证据不足以下结论，明确说明还需检查什么，不要硬下结论；\n"
    "4. 给出可执行的处置步骤（面向运维人员，具体到菜单/表/任务），遵守知识库给出的允许/禁止"
    "条件、副作用与回退边界，并在必要时说明恢复验证方法。\n"
    "必须只输出一个 JSON 对象，不要输出多余文字，字段如下：\n"
    '{"root": "一句话根因（问题是什么）", '
    '"actions": ["处置步骤1", "处置步骤2"], '
    '"confidence": 0.0到1.0的置信度, '
    '"need_more_evidence": false, '
    '"evidence_note": "关键依据，引用查到的数据与知识库分支"}'
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
        "【机器学习召回的历史相似案例（先验）】\n%s\n\n"
        "【Dimple 官方知识库·领域诊断卡（机制与处置手册，未现场核实）】\n%s\n\n"
        "【系统只读 SQL 查库证据（现场事实，以此为准）】\n%s\n\n"
        "请综合以上三类证据，用现场查库事实验证或排除知识库候选分支，输出根因与处置 JSON。"
        % (
            ctx.get("ldate", ""),
            ctx.get("errcode", ""),
            ctx.get("location", ""),
            ctx.get("text", ""),
            ctx.get("biz_type", "未知"),
            param_text,
            _fmt_cases(ctx.get("cases")),
            KnowledgeClient.to_prompt_block(ctx.get("kb_card")),
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
