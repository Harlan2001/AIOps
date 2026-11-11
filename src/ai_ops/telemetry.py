# -*- coding: utf-8 -*-
"""诊断链观测基线（工程方案 3.1）：LLM 降本率与兜底原因聚合。

口径（必须保持确定性，供汇报与后续增强决策）：
- 总诊断数 = 完整诊断链（pipeline.diagnose）处理条数；
- 规则快速路径 = telemetry.path ∈ {noise_ora, rule_fast, force_fast}：零 token；
- LLM 调用数 = telemetry.llm_called（含调用后失败回退）；
- 降本率 = 规则快速路径数 / 总诊断数；
- 兜底原因分桶（LLM 调用时）：no_type=类型未覆盖（常规入口）、
  force_llm=显式强制、llm_unavailable=调用后无结果回退。
"""
FAST_PATHS = {"noise_ora", "rule_fast", "force_fast"}


def summarize(results):
    """聚合 pipeline.diagnose 结果列表 -> 观测统计 dict。"""
    total = len(results)
    fast = sum(1 for r in results if (r.get("telemetry") or {}).get("path") in FAST_PATHS)
    llm_called = sum(1 for r in results if (r.get("telemetry") or {}).get("llm_called"))
    reasons = {}
    for r in results:
        t = r.get("telemetry") or {}
        if t.get("llm_called"):
            k = t.get("fallback_reason") or "unknown"
            reasons[k] = reasons.get(k, 0) + 1
    return {
        "total": total,
        "fast": fast,
        "llm_called": llm_called,
        "save_rate": (fast / total) if total else 0.0,
        "fallback_reasons": reasons,
    }


def format_summary(s):
    """观测统计 -> 一行文本（CLI 批量回放尾部输出）。"""
    total = s["total"]
    if not total:
        return "（无诊断记录，无观测数据）"
    reasons = "，".join("%s=%d" % (k, v) for k, v in sorted(s["fallback_reasons"].items()))
    line = ("【诊断链观测】总 %d｜规则快速路径 %d（%.1f%%）｜LLM 调用 %d（%.1f%%）｜降本率 %.1f%%"
            % (total, s["fast"], 100.0 * s["fast"] / total,
               s["llm_called"], 100.0 * s["llm_called"] / total,
               100.0 * s["save_rate"]))
    if reasons:
        line += "｜LLM 兜底原因：" + reasons
    return line
