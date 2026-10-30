# -*- coding: utf-8 -*-
"""AIOps 智能诊断工作台 —— GaussDB 信创版（Streamlit 演示）。

渲染层：本文件只负责 Streamlit UI；业务逻辑在 ai_ops.service（服务层）。

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
    """缓存诊断服务实例（含规则引擎 / 知识库 / ML 相似案例索引）。"""
    return DiagnosticService()


def gauss_check(force=False):
    """GaussDB TCP 预检（结果缓存于会话，1.5s）。"""
    s = st.session_state
    if not force and "gauss_ok" in s:
        return s["gauss_ok"], s.get("gauss_msg", "")
    info = DiagnosticService.check_gauss()
    s["gauss_ok"], s["gauss_msg"], s["gauss_checked"] = info["ok"], info["msg"], info["checked"]
    return info["ok"], info["msg"]


def render_one(rec, res):
    cls = res.get("class")
    st.markdown("**报错文本**：%s" % rec.get("text", ""))
    st.caption("时间：%s ｜ 来源：%s" % (rec.get("ldate") or "-",
               (rec.get("source_label") or rec.get("source") or "文本直输")))
    if cls in ("noise", "ora", "other") or "type" not in res:
        st.info(res.get("verdict", ""))
        return
    t = res.get("type") or {}
    st.markdown("**问题类型**：%s（%s）" % (t.get("title"), t.get("id")))

    # 证据表
    for ev in res.get("evidence", []):
        r = ev.get("r", {})
        if r.get("status") == "missing_params":
            st.markdown("- **%s**：缺少参数 %s，跳过" % (ev.get("title"),
                        "、".join(r.get("missing", []))))
            continue
        rows = r.get("rows", [])
        st.markdown("- **%s**：%d 行" % (ev.get("title"), len(rows)))
        if rows:
            st.dataframe(pd.DataFrame(rows, columns=r.get("cols")),
                         use_container_width=True, hide_index=True)

    st.markdown("#### 问题是什么")
    st.write(res.get("root", ""))
    for sec in res.get("secondary", []):
        st.caption("附带发现（%s）：%s" % (sec.get("title"), sec.get("root")))
    st.markdown("#### 怎么解决")
    for i, a in enumerate(res.get("action", []), 1):
        st.markdown("%d. %s" % (i, a))

    # 知识库机制卡（数据获取在服务层，页面只负责展示）
    svc = get_service()
    kcard = svc.kb_card(rec.get("text", ""))
    if kcard and kcard.get("cards"):
        st.markdown("#### 知识库机制卡（KB 知识层）")
        for c in kcard["cards"][:3]:
            st.markdown("- **%s**" % c["title"])
            st.caption("机制要点：" + "；".join(c["required_facts"][:4]))
            for q in c["readonly_queries"][:2]:
                st.caption("只读取证：%s（表 %s）" % (q["purpose"], q["table"]))


def sidebar():
    with st.sidebar:
        st.markdown("### 🩺 DIMPLE 诊断工作台")
        st.caption("GaussDB 信创版 · 纯规则诊断")
        st.divider()
        ok, msg = gauss_check()
        st.markdown("🟢 GaussDB 已连接" if ok else "🔴 GaussDB 未连接")
        st.caption(msg + "　·　检测于 " + st.session_state.get("gauss_checked", ""))
        if st.button("重新检测", use_container_width=True):
            gauss_check(force=True)
            st.rerun()
        st.divider()
        st.caption("诊断走 runbook 规则引擎：可解释、零 token、秒级。")


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
        run = st.button("▶ 开始诊断", type="primary", key="run_real")

    # 一键演示：敞口 / 平仓 / 策略资金不足，均为真实错误记录
    demo_key = st.session_state.get("demo")
    if demo_key in ("exposure", "close_posi", "fund"):
        st.session_state["demo"] = None
        rec = svc.demo_record(demo_key)
        pairs = svc.diagnose_many([rec]) if rec else []
    elif run:
        if trader_no and local_no:
            src = svc.sources()[source]
            key = {src.date_col: date, "trader_no": trader_no, "local_no": local_no}
            if purpose:
                key["purpose_code"] = purpose
            rec = svc.get_record(source, key)
            pairs = svc.diagnose_many([rec]) if rec else []
        else:
            recs = svc.list_records(source, date)
            pairs = svc.diagnose_many(recs)
    else:
        pairs = []

    if not pairs:
        st.info("点击「开始诊断」或上方一键演示。")
    for i, (rec, res) in enumerate(pairs):
        if len(pairs) > 1:
            st.markdown("### 记录 %d/%d" % (i + 1, len(pairs)))
        with st.container(border=True):
            render_one(rec, res)
            st.divider()
            st.caption("文本版报告：")
            st.code(reporting.render_rule(res), language="text")


def page_text():
    st.title("📝 文本诊断")
    st.caption("直接传入报错文本，用 runbook 规则诊断。")
    svc = get_service()
    with st.container(border=True):
        if st.button("演示② 结算价不存在（Au(T+D)）", use_container_width=True,
                     key="demo_settle"):
            st.session_state["text"] = "[合约=>Au(T+D)]结算价不存在"
            st.session_state["ldate"] = "20250305"
        text = st.text_area("报错文本", key="text", height=80)
        ldate = st.text_input("业务日期 YYYYMMDD", key="ldate")
        run = st.button("▶ 开始诊断", type="primary", key="run_text")

    if run and text:
        rec = {"text": text, "ldate": ldate, "errcode": 0, "lsection": ""}
        res = svc.diagnose(rec)
        with st.container(border=True):
            render_one(rec, res)
            st.divider()
            st.code(reporting.render_rule(res), language="text")


def main():
    sidebar()
    tabs = st.tabs(["① 真实报错诊断", "② 文本诊断"])
    with tabs[0]:
        page_real()
    with tabs[1]:
        page_text()


if __name__ == "__main__":
    main()
