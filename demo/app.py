# -*- coding: utf-8 -*-
"""AIOps 智能诊断工作台 —— GaussDB 信创版（Streamlit 演示）。

渲染层：本文件只负责 Streamlit UI；业务逻辑在 ai_ops.service（服务层）。
D1 方案 C：默认纯规则零 token；可选 LLM 升级（escalate，受部署 allow_escalation 约束）。

启动（仓库根）：
  uv sync --extra demo
  uv run streamlit run demo/app.py
"""
import pandas as pd
import streamlit as st

from ai_ops import reporting
from ai_ops.service import DiagnosticService, REAL_DEMOS

st.set_page_config(page_title="DIMPLE 报错智能诊断工作台（GaussDB）", page_icon="🩺", layout="wide")


@st.cache_resource(show_spinner=False)
def get_service():
    """缓存诊断服务实例（含规则引擎 / 知识库 / LLM 客户端）。"""
    return DiagnosticService()


def gauss_check(force=False):
    """GaussDB TCP 预检（结果缓存于会话，1.5s）。"""
    s = st.session_state
    if not force and "gauss_ok" in s:
        return s["gauss_ok"], s.get("gauss_msg", "")
    info = DiagnosticService.check_gauss()
    s["gauss_ok"], s["gauss_msg"], s["gauss_checked"] = info["ok"], info["msg"], info["checked"]
    return info["ok"], info["msg"]


def render_evidence(rule_res):
    """渲染规则取证证据表（数据取自契约内的 rule_res）。"""
    for ev in rule_res.get("evidence", []):
        r = ev.get("r", {})
        if r.get("status") == "missing_params":
            st.markdown("- **%s**：缺少参数 %s，跳过" % (ev.get("title"),
                        "、".join(r.get("missing", []))))
            continue
        if r.get("status") == "error":
            st.markdown("- **%s**：⚠ 取证失败（%s）" % (ev.get("title"),
                        r.get("error", "")))
            continue
        rows = r.get("rows", [])
        st.markdown("- **%s**：%d 行" % (ev.get("title"), len(rows)))
        if rows:
            st.dataframe(pd.DataFrame(rows, columns=r.get("cols")),
                         use_container_width=True, hide_index=True)


def render_kb_card(kb_card):
    """渲染知识库机制卡（仅升级路径可能返回）。"""
    if not kb_card or not kb_card.get("cards"):
        return
    st.markdown("#### 知识库机制卡（KB 知识层）")
    for c in kb_card["cards"][:3]:
        st.markdown("- **%s**" % c["title"])
        st.caption("机制要点：" + "；".join(c.get("required_facts", [])[:4]))
        for q in c.get("readonly_queries", [])[:2]:
            st.caption("只读取证：%s（表 %s）" % (q.get("purpose"), q.get("table")))


def render_one(rec, res):
    """渲染一条契约结果（DiagnosisResult 形状）。"""
    st.markdown("**报错文本**：%s" % rec.get("text", ""))
    st.caption("时间：%s ｜ 来源：%s" % (rec.get("ldate") or "-",
               (rec.get("source_label") or rec.get("source") or "文本直输")))
    st.caption("结论来源：%s ｜ escalated=%s" % (res.get("source"), res.get("escalated")))

    rule_res = res.get("rule_res") or {}
    t = rule_res.get("type") or {}
    if t:
        st.markdown("**问题类型**：%s（%s）" % (t.get("title"), t.get("id")))

    render_evidence(rule_res)

    # 降级可见化：缺参/失败 SQL 显式警示
    sql_errs = rule_res.get("sql_errors") or []
    missing = rule_res.get("missing_params") or []
    if sql_errs or missing:
        st.warning("**降级提示**：%d 条取证 SQL 未成功执行、%d 步缺参，本条结论可能基于不完整证据，请谨慎采信。"
                   % (len(sql_errs), len(missing)))
        for m in missing:
            st.caption("step %s：缺少参数 %s" % (m.get("step"), "、".join(m.get("missing", []))))
        for e in sql_errs:
            st.caption("step %s：%s" % (e.get("step"), e.get("error", "")))

    answer = res.get("answer") or {}
    st.markdown("#### 问题是什么")
    st.write(answer.get("root", ""))
    if answer.get("evidence_note"):
        st.caption(answer["evidence_note"])
    for sec in answer.get("secondary", []):
        st.caption("附带发现（%s）：%s" % (sec.get("title"), sec.get("root")))
    st.markdown("#### 怎么解决")
    actions = answer.get("actions", [])
    if actions:
        for i, a in enumerate(actions, 1):
            st.markdown("%d. %s" % (i, a))
    else:
        st.caption("（无规则处置动作，按上述排查方向人工确认）")

    render_kb_card(res.get("kb_card"))


def sidebar():
    with st.sidebar:
        st.markdown("### 🩺 DIMPLE 诊断工作台")
        st.caption("GaussDB 信创版 · 默认纯规则 · 可选 LLM 升级")
        st.divider()
        ok, msg = gauss_check()
        st.markdown("🟢 GaussDB 已连接" if ok else "🔴 GaussDB 未连接")
        st.caption(msg + "　·　检测于 " + st.session_state.get("gauss_checked", ""))
        if st.button("重新检测", use_container_width=True):
            gauss_check(force=True)
            st.rerun()
        st.divider()
        st.caption("默认走 runbook 规则引擎：可解释、零 token、秒级；显式升级才可能调 LLM。")


def _run_path(svc, recs, escalate):
    """统一诊断入口：升级受部署允许位约束，未允许则提示并纯规则。"""
    do_escalate = escalate and svc.escalation_allowed()
    if escalate and not do_escalate:
        st.warning("当前部署未启用 LLM 升级（allow_escalation=false），已按纯规则诊断。")
    pairs = svc.diagnose_many_isolated(recs, [do_escalate] * len(recs))
    return pairs


def page_real():
    st.title("🔍 真实报错诊断（GaussDB 错误历史表）")
    st.caption("选择错误来源与日期，从 GaussDB 取数并用 runbook 规则诊断；可填主键定位单条。")

    svc = get_service()
    with st.container(border=True):
        for label, key, _ in REAL_DEMOS:
            if st.button(label, use_container_width=True, key="demo_" + key):
                st.session_state["demo"] = key
        c1, c2 = st.columns(2)
        source = c1.selectbox("错误来源", list(svc.sources()),
                              format_func=lambda s: "%s（%s）" % (s, svc.sources()[s].label))
        date = c2.text_input("业务日期 YYYYMMDD", value="20250304")
        c3, c4, c5 = st.columns(3)
        trader_no = c3.text_input("交易员（可选）")
        local_no = c4.text_input("本地委托号（可选）")
        purpose = c5.text_input("交易目的（可选）")
        escalate = st.checkbox("允许 LLM 升级（逐条显式；整表回放默认不扇出）", value=False)
        run = st.button("▶ 开始诊断", type="primary", key="run_real")

    # 一键演示：敞口 / 平仓 / 策略资金不足，均为真实错误记录
    demo_key = st.session_state.get("demo")
    if demo_key in ("exposure", "close_posi", "fund"):
        st.session_state["demo"] = None
        rec = svc.demo_record(demo_key)
        pairs = _run_path(svc, [rec], escalate) if rec else []
    elif run:
        if trader_no and local_no:
            src = svc.sources()[source]
            key = {src.date_col: date, "trader_no": trader_no, "local_no": local_no}
            if purpose:
                key["purpose_code"] = purpose
            rec = svc.get_record(source, key)
            pairs = _run_path(svc, [rec], escalate) if rec else []
        else:
            recs = svc.list_records(source, date, limit=200)
            # 整表回放：纯规则，不做 LLM 扇出
            pairs = svc.diagnose_many_isolated(recs)
    else:
        pairs = []

    if not pairs:
        st.info("点击「开始诊断」或上方一键演示。")
    for i, (rec, res) in enumerate(pairs):
        if len(pairs) > 1:
            st.markdown("### 记录 %d/%d" % (i + 1, len(pairs)))
        with st.container(border=True):
            if isinstance(res, dict) and res.get("_diagnose_error"):
                st.error("本条诊断异常：%s" % res["_diagnose_error"])
                continue
            render_one(rec, res)
            st.divider()
            st.caption("文本版报告：")
            st.code(reporting.render_rule(res.get("rule_res")), language="text")


def page_text():
    st.title("📝 文本诊断")
    st.caption("直接传入报错文本，用 runbook 规则诊断；可显式升级 LLM。")
    svc = get_service()
    with st.container(border=True):
        if st.button("演示② 结算价不存在（Au(T+D)）", use_container_width=True,
                     key="demo_settle"):
            st.session_state["text"] = "[合约=>Au(T+D)]结算价不存在"
            st.session_state["ldate"] = "20250305"
        text = st.text_area("报错文本", key="text", height=80)
        ldate = st.text_input("业务日期 YYYYMMDD", key="ldate")
        escalate = st.checkbox("允许 LLM 升级（escalate）", value=False)
        run = st.button("▶ 开始诊断", type="primary", key="run_text")

    if run and text:
        rec = {"text": text, "ldate": ldate, "errcode": 0, "lsection": ""}
        pairs = _run_path(svc, [rec], escalate)
        _rec, res = pairs[0]
        with st.container(border=True):
            render_one(rec, res)
            st.divider()
            st.code(reporting.render_rule(res.get("rule_res")), language="text")


def main():
    sidebar()
    tabs = st.tabs(["① 真实报错诊断", "② 文本诊断"])
    with tabs[0]:
        page_real()
    with tabs[1]:
        page_text()


if __name__ == "__main__":
    main()
