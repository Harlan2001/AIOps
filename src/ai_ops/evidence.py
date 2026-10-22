# -*- coding: utf-8 -*-
"""知识卡中立格式化：card dict -> 提示词块 / CLI 报告行。

放在 kb 适配器之外，使 llm.prompts 不再反向依赖 kb 客户端；
KnowledgeClient 只负责检索与裁剪，格式化在这里。
"""
_TXT_LIMIT = 200


def clip(s, n=_TXT_LIMIT):
    s = str(s or "").replace("\n", " ").strip()
    return s if len(s) <= n else s[:n] + "…"


def join(items, n=None):
    if isinstance(items, str):
        return items.strip()
    items = [str(x).strip() for x in (items or []) if str(x).strip()]
    if n:
        items = items[:n]
    return "；".join(items)


def to_prompt_block(card):
    if not card or not card.get("cards"):
        return "（知识库未命中相关诊断材料，本条请主要依据历史案例与现场查库证据判断。）"
    L = []
    L.append(
        "以下是 Dimple 官方知识库（版本 %s，源码基线 %s）按症状检索到的诊断材料，"
        "共命中相关父文档 %d 篇。\n"
        "重要约束：这是【冻结源码取证】，runtime_verified=%s，未在现场核实；"
        "其中只读 SQL 未在现场执行，不得声称已执行、不得据此臆测现场状态。"
        "请用下面系统实际查到的库内证据去验证或排除这些候选分支，"
        "处置建议必须遵守其允许/禁止条件、副作用与回退边界。"
        % (card.get("knowledge_version", ""), card.get("baseline_id", ""),
           card.get("matched_document_count", 0),
           "true" if card.get("runtime_verified") else "false"))
    for i, c in enumerate(card["cards"], 1):
        L.append("\n[知识卡 %d] %s（文档 ID：%s，得分 %.1f）"
                 % (i, c["title"], c["document_id"], c["score"]))
        if c["symptom"]:
            L.append("  症状：%s" % clip(c["symptom"], 160))
        if c["required_facts"]:
            L.append("  必须先确认的事实：" + join(c["required_facts"], 14))
        if c["parameter_codes"]:
            L.append("  相关参数：" + "、".join(map(str, c["parameter_codes"])))
        for b in c["branches"]:
            L.append("  ◆ 候选根因分支：%s" % b["id"])
            if b["when_all"]:
                L.append("      成立条件：" + join(b["when_all"]))
            if b["exclude_when"]:
                L.append("      反证/不适用：" + join(b["exclude_when"]))
            if b["next_checks"]:
                L.append("      下一步只读检查：" + join(b["next_checks"]))
            for a in b["actions"]:
                if a["title"]:
                    L.append("      候选处置：%s" % a["title"])
                if a["allowed_when"]:
                    L.append("          允许条件：" + join(a["allowed_when"]))
                if a["forbidden_when"]:
                    L.append("          禁止条件：" + join(a["forbidden_when"]))
                if a["side_effects"]:
                    L.append("          副作用：" + join(a["side_effects"]))
                if a["verification"]:
                    L.append("          恢复验证：" + join(a["verification"]))
                if a["rollback_boundary"]:
                    L.append("          回退边界：" + join(a["rollback_boundary"]))
        for q in c["readonly_queries"]:
            L.append("  只读SQL参考（%s，表 %s，方言 %s；需现场核对，禁止擅自执行）：%s"
                     % (q["purpose"] or "-", q["table"] or "-",
                        q["dialect"] or "-", q["sql"]))
            if q["interpretation"]:
                L.append("      结果解释：%s" % clip(q["interpretation"], 300))
        for lg in c["log_context"]:
            L.append("  日志锚点（%s/%s）：%s"
                     % (lg.get("logger", ""), lg.get("level", ""),
                        clip(lg.get("template", ""), 160)))
    return "\n".join(L)


def to_report_lines(card):
    if not card or not card.get("cards"):
        return ["  （知识库未命中相关诊断材料）"]
    L = ["  知识版本 %s｜基线 %s｜相关父文档 %d 篇｜状态：冻结源码取证，未现场核实"
         % (card.get("knowledge_version", ""), card.get("baseline_id", ""),
            card.get("matched_document_count", 0))]
    for i, c in enumerate(card["cards"], 1):
        L.append("  %d. [%.1f] %s（%s）" % (i, c["score"], c["title"], c["document_id"]))
        L.append("       症状：%s" % (clip(c["symptom"], 120) or "-"))
        for b in c["branches"][:3]:
            L.append("       · 根因分支 %s：%s"
                     % (b["id"], clip(join(b["when_all"], 3), 120)))
        if c["required_facts"]:
            L.append("       · 需先确认：%s" % clip(join(c["required_facts"], 6), 200))
        L.append("       · 取证材料：只读SQL模板 %d 条、日志锚点 %d 处（默认不自动执行）"
                 % (c["n_queries"], c["n_logs"]))
        if c["sources"]:
            s = c["sources"][0]
            L.append("       · 来源：%s %s %s"
                     % (s.get("repository", ""), s.get("path", ""), s.get("symbol", "")))
    return L
