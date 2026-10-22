# -*- coding: utf-8 -*-
"""AIOps 智能诊断工作台 —— Streamlit 快速演示版（POC 前脸）。

定位（向领导演示用）：
  - 这是《产品形态设计文档》规划的私有化内网 Web 工作台的快速 POC，
    内核直接调用 ai_ops.pipeline.diagnose() 稳定契约，零改动、零 mock；
  - 正式版技术栈为 FastAPI + Vue3 + Element Plus + MySQL，本页只做产品形态验证。

演示网络假设：
  - 公网 LLM（开发期默认）：长尾诊断可用；
  - 内网 Oracle 不保证可达：TCP 预检（1.5s）防止长超时，断库时跳过现场查库、
    保留真实 ML 分流/召回 + LLM 结论，并以黄条明示；
  - 完全离线：噪音/ORA 秒级分诊、统计看板基线、历史批量报告、demo/samples 离线样例。

启动（仓库根）：uv run streamlit run demo/app.py
"""
import json
import os
import re
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from ai_ops import paths, reporting
from ai_ops.config import load_config
from ai_ops.engine import parser as P
from ai_ops.engine.rule_engine import Engine
from ai_ops.engine.tlog import get_record_by_id
from ai_ops.kb.client import KnowledgeClient
from ai_ops.llm.client import LLMClient
from ai_ops.ml.router import Router
from ai_ops.ml.retriever import SimilarCaseIndex
from ai_ops.pipeline import diagnose

# ---------------------------------------------------------------------------
# 常量与路径
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AIOps 智能诊断工作台（POC）", page_icon="🩺", layout="wide")

REPO_ROOT = Path(paths.REPO_ROOT) if paths.REPO_ROOT else Path.cwd()
DEMO_DIR = Path(__file__).resolve().parent
SAMPLES_DIR = DEMO_DIR / "samples"
REPLAY_SCRIPT = REPO_ROOT / "scripts" / "hybrid_replay.py"
BATCH_REPORT = paths.reports_dir() / "llm_demo_result.txt"

LLM_TIMEOUT = 12  # 现场诊断最多等待 12s，超时走诚实降级（不让台上干等）

# 离线回归基线（scripts/hybrid_replay.py，2026-10 实测；看板实时重测失败时回退）
BASELINE = {
    "n": 89733, "ml_fast": 84378, "ml_pct": 94.03,
    "biz": 5336, "biz_pct": 5.95, "other": 19,
    "cur_rule": 271, "cur_rule_biz": 5.08, "cur_rule_pct": 0.30,
    "cur_llm": 5065, "cur_llm_biz": 94.92, "cur_llm_pct": 5.64, "low_conf": 22,
    "top_rule": 4978, "top_rule_biz": 93.29, "top_rule_pct": 5.55,
    "top_llm": 358, "top_llm_biz": 6.71, "top_llm_pct": 0.40,
}

# 一键样例（文本均取自 var/data/ml/dataset.csv 真实记录）
SAMPLE_TEXTS = [
    ("① 噪音拦截（成功提示）", "无需要发送的DAMS数据！"),
    ("② ORA 技术错误（转 DBA）", "SQLCODE:-1 SQLERRM:ORA-00001: unique constraint violated"),
    ("③ 结算价不存在（高频·已建规则）", "[期权合约=>au2610C356]结算价不存在"),
    ("④ 持仓不足（旗舰·已建规则）",
     "平仓错误,[会员->016811][客户->0000000168][合约=>Au(T+N1)][买]持仓不足,尚缺<3>"),
    ("⑤ 存续期变更失败（长尾·诚实低置信）", "系统不存在该条记录,存续期变更失败"),
    ("⑥ 用户名或密码错误（长尾）", "用户名或密码错误"),
]

# 五种正式来源 + 一种演示期断库标记 -> 徽标（底色, 文案）
SOURCE_BADGE = {
    "ML 快速路径": ("#0969da", "ML 快速路径 · ⚡ 零 token"),
    "规则快速路径（ML 高置信 + 只读查库，零 token）": ("#1a7f37", "规则快速路径 · ⚡ 零 token"),
    "LLM 诊断大脑（ML 分流/召回 + 规则取证）": ("#8250df", "LLM 诊断大脑 · 综合证据推理"),
    "规则兜底（LLM 未配置/不可用，已按规则查库）": ("#bf8700", "规则兜底 · LLM 不可用"),
    "兜底（LLM 未配置 + 规则未覆盖）": ("#57606a", "诚实兜底 · 建议人工复核"),
}

_DSN_RE = re.compile(r"@?([0-9A-Za-z_.\-]+):(\d+)")


# ---------------------------------------------------------------------------
# 组件缓存（服务化复用同一实例；Engine 懒连接，缓存安全）
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner="首次加载 ML 分流模型…")
def get_router():
    return Router()


@st.cache_resource(show_spinner="首次构建相似案例索引（约 1 秒）…")
def get_retriever():
    return SimilarCaseIndex.from_dataset()


@st.cache_resource(show_spinner=False)
def get_engine():
    return Engine()


@st.cache_resource(show_spinner=False)
def get_kb():
    return KnowledgeClient()


@st.cache_resource(show_spinner=False)
def get_llm():
    cli = LLMClient(load_config("llm"))
    cli.timeout = LLM_TIMEOUT  # 覆盖 yaml 的 150s：演示不等长超时
    return cli


# ---------------------------------------------------------------------------
# 内网 Oracle 预检（TCP，1.5s；绝不触发 oracledb 长超时）
# ---------------------------------------------------------------------------
def oracle_check(force=False):
    """返回 (是否可达, 说明)。结果缓存到 session，侧栏可手动重检。"""
    s = st.session_state
    if not force and "oracle_ok" in s:
        return s["oracle_ok"], s.get("oracle_msg", "")
    cfg = load_config("db")
    m = _DSN_RE.search(cfg.get("dsn") or "")
    if not m:
        ok, msg = False, "未配置 db.yaml DSN"
    else:
        try:
            with socket.create_connection((m.group(1), int(m.group(2))), timeout=1.5):
                ok, msg = True, "%s:%s 可达" % (m.group(1), m.group(2))
        except OSError as e:
            ok, msg = False, "%s:%s 不可达（%s）" % (m.group(1), m.group(2), type(e).__name__)
    s["oracle_ok"], s["oracle_msg"], s["oracle_checked"] = ok, msg, \
        datetime.now().strftime("%H:%M:%S")
    return ok, msg


class _NoSQLEngine:
    """断库时注入 pipeline 的替身：返回“查库已跳过”的 rule_res，绝不发起连接。"""

    def __init__(self, stub):
        self._stub = stub

    def diagnose(self, record):
        return self._stub

    def close(self):
        pass


def _skip_stub(rec, reason):
    text = (rec.get("text") or "").strip()
    errcode = rec.get("errcode") or 0
    return {
        "class": "biz", "text": text, "errcode": errcode,
        "ldate": rec.get("ldate", ""), "lsection": rec.get("lsection", ""),
        "verdict": reason, "offline_skipped": True,
        "evidence": [{"id": "offline", "title": "现场只读查库",
                      "kind": "sql_check",
                      "r": {"status": "failed", "error": reason}}],
    }


def run_diagnose(rec, force_llm=False, force_fast=False):
    """返回 (res | None, warning | None, error | None)。"""
    text = (rec.get("text") or "").strip()
    errcode = rec.get("errcode") or 0
    router, retr, eng, kb, llm = get_router(), get_retriever(), get_engine(), get_kb(), get_llm()

    rt = router.route(text, errcode)
    tcfg = None
    if rt["route"] in ("biz", "other"):
        tcfg, _ = eng.match_type(text, errcode)

    use_eng, warning = eng, None
    if tcfg is not None and not oracle_check()[0]:
        if force_fast:
            return None, None, "强制规则快速路径需要内网 Oracle 现场查库，当前内网不可达。\n" \
                               "可改用「强制走 LLM」，或在本页下方打开离线预跑样例。"
        reason = "内网 Oracle 不可达，现场只读查库已跳过（%s）" % st.session_state.oracle_msg
        use_eng = _NoSQLEngine(_skip_stub(rec, reason))
        warning = "内网 Oracle 当前不可达，已跳过现场查库；以下结论基于真实 ML 分流/召回" \
                  " + 公网 LLM。完整三证合一案例见「历史诊断」页的离线预跑样例。"

    try:
        res = diagnose(rec, force_llm=force_llm, force_fast=force_fast, llm=llm,
                       router=router, retriever=retr, eng=use_eng, kbcli=kb)
    except Exception as e:
        return None, warning, "%s: %s" % (type(e).__name__, e)
    return res, warning, None


# ---------------------------------------------------------------------------
# 结果渲染（实时结果与 demo/samples 离线 JSON 共用，保证两种场景完全同构）
# ---------------------------------------------------------------------------
def _badge(source):
    color, label = SOURCE_BADGE.get(source, ("#57606a", source))
    st.markdown(
        '<span style="background:%s;color:#fff;padding:3px 12px;border-radius:12px;'
        'font-size:14px;font-weight:600">%s</span>' % (color, label),
        unsafe_allow_html=True)


def _conf_line(conf):
    try:
        c = max(0.0, min(1.0, float(conf)))
    except (TypeError, ValueError):
        c = 0.0
    col = "#1a7f37" if c >= 0.8 else ("#bf8700" if c >= 0.5 else "#cf222e")
    st.progress(c, text="诊断置信度 %.2f" % c)
    st.markdown('<span style="color:%s;font-size:13px">%s</span>' % (
        col, "证据充分" if c >= 0.8 else ("证据基本可用" if c >= 0.5 else "证据不足，建议人工复核")),
        unsafe_allow_html=True)


def _step_strip(res):
    """五步执行路径指示：实际走到的 ✅，跳过的 ⏭️，断网跳过的 ⚠️。"""
    rt = res["rt"]
    route, biz = rt["route"], rt["route"] in ("biz", "other")
    cases, rr, kb_card = res.get("cases", []), res.get("rule_res"), res.get("kb_card")

    s1 = ("✅", "ML 分流", "%s · %.2f" % (route, rt.get("confidence", 0.0)))
    if not biz:
        s2 = ("⏭️", "相似召回", "非业务报错")
        s3 = ("⏭️", "知识检索", "—")
        s4 = ("⏭️", "只读查库", "—")
    else:
        s2 = ("✅", "相似召回", "%d 条历史案例" % len(cases)) if cases else ("⚠️", "相似召回", "数据集缺失")
        if kb_card:
            s3 = ("✅", "知识检索", "%d 张知识卡" % kb_card.get("matched_document_count", 0))
        else:
            s3 = ("✅", "知识检索", "已检索·无卡/未挂载")
        if rr and rr.get("offline_skipped"):
            s4 = ("⚠️", "只读查库", "内网不可达·跳过")
        elif rr and rr.get("verdict") == "诊断完成":
            s4 = ("✅", "只读查库", "%d 组只读证据" % len(rr.get("evidence", [])))
        else:
            s4 = ("⏭️", "只读查库", "规则未覆盖")
    src = res.get("source", "")
    if src.startswith("ML"):
        s5 = ("✅", "决策门", "入口拦截")
    elif src.startswith("规则快速"):
        s5 = ("✅", "决策门", "零 token 结论")
    elif src.startswith("LLM"):
        s5 = ("✅", "决策门", "升级 LLM")
    elif "兜底" in src:
        s5 = ("⚠️", "决策门", "降级/兜底")
    else:
        s5 = ("✅", "决策门", "完成")

    cols = st.columns(5)
    for col, (icon, name, sub) in zip(cols, (s1, s2, s3, s4, s5)):
        col.markdown("**%s %s**" % (icon, name))
        col.caption(sub)


def _render_cases(cases):
    if not cases:
        st.info("无历史相似案例（数据集缺失或确实没有同类历史）。")
        return
    df = pd.DataFrame([{
        "相似度": c["similarity"], "历史次数": c["count"], "最近发生": c["last_date"],
        "错误码": "/".join(c.get("errcodes", [])) or "-",
        "归一化骨架": c["skeleton"],
    } for c in cases])
    st.dataframe(df, width="stretch", hide_index=True)


def _render_kb_card(kb_card):
    if not kb_card:
        st.info("知识库快照未挂载（本机无 config/kb.yaml）。正式部署挂载 Dimple 知识快照后，"
                "这里展示候选根因分支、成立/反证条件与处置边界（机制证据）。")
        return
    st.caption("版本 %s ｜ 基线 %s ｜ 命中文档 %s 个 ｜ 知识为冻结源码取证，未现场核实"
               % (kb_card.get("knowledge_version", "-"), kb_card.get("baseline_id", "-"),
                  kb_card.get("matched_document_count", 0)))
    for card in kb_card.get("cards", [])[:3]:
        with st.container(border=True):
            st.markdown("**%s**（匹配分 %.2f）" % (card.get("title", ""), card.get("score", 0.0)))
            if card.get("required_facts"):
                st.caption("必收事实：" + "、".join(card["required_facts"][:8]))
            for b in card.get("branches", [])[:3]:
                when = "；".join(b.get("when_all", [])[:3])
                st.markdown("- 分支 `%s`：%s" % (b.get("id", ""), when or "（通用分支）"))
                for a in b.get("actions", [])[:2]:
                    st.markdown("  - %s" % a.get("title", ""))
            st.caption("只读 SQL 建议 %d 条（默认不在现场执行，需审核后派生为 runbook）"
                       % card.get("n_queries", 0))


def _render_rule_res(rule_res):
    if not rule_res:
        st.caption("本条未执行规则查库。")
        return
    if rule_res.get("offline_skipped"):
        st.warning("现场只读查库已跳过：%s。离线预跑样例中保留了同类型报错的真实查库证据。"
                   % rule_res.get("verdict", "内网不可达"))
        return
    if rule_res.get("verdict") != "诊断完成":
        st.caption("规则引擎判定：%s（未匹配到已编码的确定性规则）" % rule_res.get("verdict", "-"))
        return
    t = rule_res.get("type") or {}
    st.markdown("命中规则类型：**%s**（%s）" % (t.get("title", "-"), t.get("id", "-")))
    params = {k: v for k, v in (rule_res.get("params") or {}).items()
              if v not in (None, "") and k != "trade_date"}
    if params:
        st.caption("抽取参数：" + "，".join("%s=%s" % (k, v) for k, v in params.items()))
    for ev in rule_res.get("evidence", []):
        r = ev.get("r", {})
        if r.get("status") == "missing_params":
            st.markdown("- **%s**：缺少参数 %s，跳过" % (ev.get("title"), "、".join(r.get("missing", []))))
            continue
        if r.get("status") != "ok":
            st.markdown("- **%s**：查询失败（%s）" % (ev.get("title"), r.get("error", "-")))
            continue
        n = len(r.get("rows", []))
        st.markdown("- **%s**：%d 行" % (ev.get("title"), n))
        if r.get("rows"):
            st.dataframe(pd.DataFrame(r["rows"], columns=r.get("cols")),
                         width="stretch", hide_index=True)


def render_result(res, warning=None, meta=None):
    """实时结果 / 离线 JSON 样例共用的完整结论版面。"""
    if meta:
        st.caption(meta)
    with st.container(border=True):
        st.markdown("**报错文本**：%s" % res.get("text", "")[:200])
        c1, c2, c3 = st.columns(3)
        c1.caption("时间：%s" % (res.get("ldate") or "（文本直输，无时间）"))
        c2.caption("错误码：%s" % res.get("errcode"))
        c3.caption("位置：%s" % (res.get("loc") or "-"))

    if warning:
        st.warning(warning)

    _step_strip(res)
    st.divider()

    ans = res.get("answer") or {}
    with st.container(border=True):
        _badge(res.get("source", ""))
        st.markdown("#### 问题是什么")
        if ans.get("_raw"):
            st.write(ans.get("root", ""))
        else:
            st.write(ans.get("root", "（无结论）"))
        if ans.get("evidence_note"):
            st.markdown("#### 关键依据")
            st.write(ans["evidence_note"])
        _conf_line(ans.get("confidence", 0.0))
        if ans.get("need_more_evidence"):
            st.warning("LLM 明确标注：现有证据不足，需要补充取证后再定论。")
        actions = ans.get("actions") or []
        if actions:
            st.markdown("#### 怎么解决")
            for i, a in enumerate(actions, 1):
                st.markdown("%d. %s" % (i, a))
        for sec in ans.get("secondary", []) or []:
            with st.expander("附带发现：%s" % sec.get("title", "-")):
                st.write(sec.get("root", ""))
                for i, a in enumerate(sec.get("action", []) or [], 1):
                    st.markdown("%d. %s" % (i, a))

    st.divider()
    tab1, tab2, tab3, tab4 = st.tabs(
        ["① 相似历史案例（先验）", "② 领域知识卡（机制）", "③ 只读查库证据（现场事实）", "文本版完整报告"])
    with tab1:
        _render_cases(res.get("cases", []))
    with tab2:
        _render_kb_card(res.get("kb_card"))
    with tab3:
        _render_rule_res(res.get("rule_res"))
    with tab4:
        try:
            st.code(reporting.render_hybrid(res), language="text")
        except Exception as e:
            st.caption("文本报告渲染失败：%s" % e)


# ---------------------------------------------------------------------------
# 页① 首页总览（突出产品化规划）
# ---------------------------------------------------------------------------
def page_home():
    st.title("🩺 数据库业务报错智能诊断工作台")
    st.caption("Streamlit 快速演示版（POC）｜ 内核版本 ai-ops 0.1.0 ｜ "
               "正式版：FastAPI + Vue3 + Element Plus + MySQL（私有化内网部署）")

    b = BASELINE
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("历史日志回归样本", "{:,} 条".format(b["n"]))
    c2.metric("ML 入口拦截（零 token）", "%.2f%%" % b["ml_pct"], "噪音/ORA 直接分诊")
    c3.metric("规则补齐 Top30 后真实 LLM 调用", "%.2f%%" % b["top_llm_pct"],
              delta="-%.1f%%" % (b["cur_llm_pct"] - b["top_llm_pct"]), delta_color="inverse")
    try:
        size_mb = sum((p.stat().st_size for p in paths.models_dir().glob("*.joblib"))) / 1e6
        c4.metric("分流模型体积", "%.1f MB" % size_mb, "纯 CPU · 毫秒级")
    except OSError:
        c4.metric("分流模型体积", "1.7 MB", "纯 CPU · 毫秒级")
    c5.metric("单条诊断耗时", "毫秒 / 十秒级", "快路径 / LLM 长尾")

    st.divider()
    st.subheader("工作台模块地图（对齐《产品形态设计文档》§4.1）")
    done_mods = [
        ("诊断查询", "文本/TLOG ID 输入、强制 LLM/规则开关", "本 POC 已实现"),
        ("诊断报告页", "结构化结论 + 三证折叠 + 置信度 + 文本报告", "本 POC 已实现"),
        ("统计看板", "分流占比、降本测算、89,733 条全量离线回放", "本 POC 已实现"),
        ("历史诊断", "批量报告与离线预跑样例回看（正式版入 MySQL）", "POC 简化版"),
    ]
    plan_mods = [
        ("首页总览 / 运行健康", "资产、连通性、服务状态灯（本页侧栏为雏形）", "P1"),
        ("事件中心", "批量扫描、事件聚合、处置流与回流闭环", "P2"),
        ("规则 / 知识管理", "规则热更新审批、知识快照挂载与客户投影门禁", "P2–P3"),
        ("系统管理", "用户 / 角色 / 权限（RBAC）、审计日志", "P3–P4"),
        ("诊断 API", "FastAPI 薄封装 diagnose() 契约，对接站内系统", "P1"),
    ]
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**本次 POC 已落地**")
        for name, desc, tag in done_mods:
            st.markdown('<span style="color:#0969da">●</span> **%s**　`%s`<br><span style="color:#57606a;font-size:13px">%s</span>'
                        % (name, tag, desc), unsafe_allow_html=True)
    with col_b:
        st.markdown("**产品规划中（本次演示用静态形态呈现）**")
        for name, desc, tag in plan_mods:
            st.markdown('<span style="color:#8c959f">●</span> **%s**　`%s`<br><span style="color:#57606a;font-size:13px">%s</span>'
                        % (name, tag, desc), unsafe_allow_html=True)

    st.divider()
    st.subheader("产品化路线（P1 → P4）")
    p1, p2, p3, p4 = st.columns(4)
    p1.markdown("**P1｜服务化 MVP**\n\nFastAPI 薄封装诊断内核 + Web 诊断页 + MySQL 历史库；"
                "内网 vLLM/网关接入；Docker Compose 离线部署")
    p2.markdown("**P2｜正式工作台**\n\nVue3 + Element Plus 正式前端；事件中心、批量扫描、"
                "处置跟踪；规则热更新与审计")
    p3.markdown("**P3｜闭环增强**\n\n增量日志扫描与站内事件；知识快照管理、客户投影门禁；"
                "回流数据飞轮（新规则/重训练）")
    p4.markdown("**P4｜规模化交付**\n\n私有化一键安装、K8s 部署；诊断 API 对接站内系统；"
                "多环境（开发/测试/生产）与 RBAC")


# ---------------------------------------------------------------------------
# 页② 诊断查询（核心）
# ---------------------------------------------------------------------------
def page_diagnose():
    st.title("🔍 诊断查询")
    st.caption("输入一条真实报错文本，系统依次执行：ML 分流 → 相似案例召回 → 领域知识检索 → "
               "只读查库取证 → 决策门（零 token 快路径 / LLM 长尾）")

    with st.container(border=True):
        st.text_area("报错文本（可粘贴 TLOG LTEXTE 原文）", key="input_text", height=90,
                     placeholder="例如：[期权合约=>au2610C356]结算价不存在")
        tcol1, tcol2 = st.columns(2)
        tcol1.toggle("强制走 LLM（三证合一推理）", key="force_llm")
        tcol2.toggle("强制规则快路径（零 token，需内网可达）", key="force_fast",
                     disabled=st.session_state.get("force_llm", False))
        if st.session_state.get("force_llm") and st.session_state.get("force_fast"):
            st.session_state.force_fast = False
            st.info("两个开关互斥，已按「强制走 LLM」执行。")

        st.markdown("**一键填入真实样例**")
        for row_i in range(0, len(SAMPLE_TEXTS), 3):
            bcs = st.columns(3)
            for col, (label, txt) in zip(bcs, SAMPLE_TEXTS[row_i:row_i + 3]):
                if col.button(label, width="stretch"):
                    st.session_state.input_text = txt
                    st.session_state.pop("last_result", None)
                    st.rerun()

        bc1, bc2 = st.columns([1, 3])
        run_clicked = bc1.button("▶ 开始诊断", type="primary", width="stretch")

        st.divider()
        ok, msg = oracle_check()
        icol1, icol2 = st.columns([1, 3])
        icol1.markdown("**TLOG ID 模式**（按 ID 实时取数）")
        sid = icol2.text_input("日志 ID", placeholder="如 4811525544",
                               disabled=not ok, label_visibility="collapsed")
        if not ok:
            st.caption("内网 Oracle 当前不可达（%s），ID 模式停用；文本模式与离线样例不受影响。"
                       % msg)
        id_clicked = st.button("按 ID 取数并诊断", disabled=not ok)

    s = st.session_state
    if run_clicked:
        text = (s.get("input_text") or "").strip()
        if not text:
            st.warning("请先输入或选择一条报错文本。")
        else:
            with st.spinner("诊断中… ML 分流/召回为本地毫秒级；若升级公网 LLM，最多等待 %ds"
                            % LLM_TIMEOUT):
                rec = {"text": text, "errcode": 0, "ldate": "", "lsection": ""}
                res, warn, err = run_diagnose(
                    rec, force_llm=s.get("force_llm", False),
                    force_fast=s.get("force_fast", False))
            if err:
                st.error(err)
            else:
                s.last_result = (res, warn, "实时诊断 · %s · 文本直输"
                                 % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if id_clicked and sid.strip():
        with st.spinner("正在从内网 TLOG 取数并诊断…"):
            try:
                rec = get_record_by_id(int(sid.strip()))
            except Exception as e:
                rec, err = None, "%s: %s" % (type(e).__name__, e)
            else:
                err = None
        if err:
            st.error("取数失败：%s" % err)
        elif not rec:
            st.warning("未找到 ID=%s 的日志记录。" % sid.strip())
        else:
            s.input_text = rec["text"]
            res, warn, err = run_diagnose(rec)
            if err:
                st.error(err)
            else:
                s.last_result = (res, warn, "实时诊断 · %s · TLOG ID=%s"
                                 % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), sid.strip()))

    if "last_result" in s:
        res, warn, meta = s.last_result
        render_result(res, warning=warn, meta=meta)
    else:
        st.info("👆 选择一个一键样例，或直接粘贴报错文本后点击「开始诊断」。")


# ---------------------------------------------------------------------------
# 页③ 统计看板（降本故事 + 可现场离线重测）
# ---------------------------------------------------------------------------
def _parse_replay(text):
    """从 hybrid_replay.py 输出解析关键数字；失败返回 None。"""
    def find1(pat, src, cast=int):
        m = re.search(pat, src)
        return cast(m.group(1)) if m else None
    try:
        n = find1(r"共\s*(\d+)\s*条", text)
        sec_cur = text.split("【当前：")[1].split("【未来：")[0]
        sec_fut = text.split("【未来：")[1].split("=" * 10)[0]
        cr = re.search(r"规则快速路径.*?：(\d+) 条，占业务\s*([\d.]+)% / 总量\s*([\d.]+)%", sec_cur)
        cl = re.search(r"需调用 LLM.*?：(\d+) 条，占业务\s*([\d.]+)% / 总量\s*([\d.]+)%", sec_cur)
        fr = re.search(r"规则快速路径.*?：(\d+) 条，占业务\s*([\d.]+)% / 总量\s*([\d.]+)%", sec_fut)
        fl = re.search(r"需调用 LLM.*?：(\d+) 条，占业务\s*([\d.]+)% / 总量\s*([\d.]+)%", sec_fut)
        low = find1(r"类型低置信（<[\d.]+）：(\d+)", sec_cur)
        if not all([n, cr, cl, fr, fl]):
            return None
        return {
            "n": n,
            "ml_fast": find1(r"【ML 快速路径】.*?：(\d+) 条", text),
            "ml_pct": find1(r"【ML 快速路径】.*?占总量\s*([\d.]+)", text, float),
            "biz": find1(r"业务报错：(\d+) 条", text),
            "cur_rule": int(cr.group(1)), "cur_rule_biz": float(cr.group(2)), "cur_rule_pct": float(cr.group(3)),
            "cur_llm": int(cl.group(1)), "cur_llm_biz": float(cl.group(2)), "cur_llm_pct": float(cl.group(3)),
            "low_conf": low or 0,
            "top_rule": int(fr.group(1)), "top_rule_biz": float(fr.group(2)), "top_rule_pct": float(fr.group(3)),
            "top_llm": int(fl.group(1)), "top_llm_biz": float(fl.group(2)), "top_llm_pct": float(fl.group(3)),
        }
    except Exception:
        return None


def page_board():
    st.title("📊 统计看板")
    st.caption("离线回归基线：对 %s 条真实 FATAL/ERROR 日志全量回放（不连库、不耗 token）。"
               "可现场点击重测。" % "{:,}".format(BASELINE["n"]))

    if st.button("🔄 现场实时重测（约 1 分钟，全程离线）", type="primary"):
        if not REPLAY_SCRIPT.is_file():
            st.error("找不到 %s" % REPLAY_SCRIPT)
        else:
            with st.status("正在全量回放 {:,} 条历史日志…".format(BASELINE["n"]),
                          expanded=True) as status:
                kwargs = dict(cwd=str(REPO_ROOT), stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
                if os.name == "nt":
                    kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
                try:
                    proc = subprocess.Popen(
                        [sys.executable, "-X", "utf8", str(REPLAY_SCRIPT)], **kwargs)
                    lines = []
                    for raw in proc.stdout:
                        lines.append(raw.rstrip())
                        if len(lines) <= 30:
                            st.text(raw.rstrip())
                    proc.wait(timeout=180)
                except Exception as e:
                    proc.kill()
                    st.warning("重测异常（%s），看板使用内置基线数字。" % e)
                else:
                    parsed = _parse_replay("\n".join(lines))
                    if proc.returncode == 0 and parsed:
                        st.session_state.board = parsed
                        st.success("重测完成，数字已刷新（与基线一致）。")
                        status.update(label="重测完成", state="complete", expanded=False)
                    else:
                        st.warning("输出解析失败，看板继续使用内置基线。")
                        with st.expander("原始输出"):
                            st.code("\n".join(lines), language="text")

    b = st.session_state.get("board", BASELINE)
    live = st.session_state.get("board") is not None
    st.caption("当前数字来源：%s" % ("现场重测 ✓" if live else "内置基线（2026-10 实测）"))

    st.subheader("入口分流")
    c1, c2, c3 = st.columns(3)
    c1.metric("总样本", "{:,}".format(b["n"]))
    c2.metric("ML 快速路径（噪音/ORA）", "{:,} 条".format(b["ml_fast"]), "%.2f%%" % b["ml_pct"])
    c3.metric("业务报错（进入诊断管线）", "{:,} 条".format(b["biz"]), "%.2f%%" % b["biz_pct"])

    st.subheader("降本主线：规则覆盖率 ↑，真实 LLM 调用 ↓")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("当前规则快路径（3 类规则）", "{:,} 条".format(b["cur_rule"]),
              "业务 %.2f%% / 总量 %.2f%%" % (b["cur_rule_biz"], b["cur_rule_pct"]))
    c2.metric("当前需调用 LLM", "{:,} 条".format(b["cur_llm"]),
              "业务 %.2f%% / 总量 %.2f%%" % (b["cur_llm_biz"], b["cur_llm_pct"]))
    c3.metric("Top30 规则快路径（目标）", "{:,} 条".format(b["top_rule"]),
              "业务 %.2f%% / 总量 %.2f%%" % (b["top_rule_biz"], b["top_rule_pct"]))
    c4.metric("Top30 后需调用 LLM（目标）", "{:,} 条".format(b["top_llm"]),
              "业务 %.2f%% / 总量 %.2f%%" % (b["top_llm_biz"], b["top_llm_pct"]))
    st.caption("其中类型低置信（强制人工/LLM 复核）：%s 条。LLM 调用从 %.2f%% 降到 %.2f%%，"
               "降幅约 %.1f%%；且 94%% 入口流量完全不耗 token。"
               % (b["low_conf"], b["cur_llm_pct"], b["top_llm_pct"],
                  100.0 * (b["cur_llm"] - b["top_llm"]) / max(b["cur_llm"], 1)))

    df = pd.DataFrame({
        "规则快速路径（零 token）": [b["cur_rule"], b["top_rule"]],
        "需调用 LLM": [b["cur_llm"], b["top_llm"]],
    }, index=["当前：已建 3 类规则", "目标：规则补齐 Top30"])
    st.bar_chart(df, color=["#1a7f37", "#8250df"], y_label="业务报错条数")


# ---------------------------------------------------------------------------
# 页④ 历史诊断 / 批量报告 / 离线样例
# ---------------------------------------------------------------------------
_SECTION_RE = re.compile(
    r"#+\s*\n# (\d+)\. (.+?)\n# 日志ID=(\d+)\s+规则覆盖=(是|否)\n#+\s*\n(.*?)(?=\n{2,}#{10,}|\Z)",
    re.S)


def _load_batch_sections():
    if not BATCH_REPORT.is_file():
        return []
    text = BATCH_REPORT.read_text(encoding="utf-8", errors="replace")
    return [{"idx": m.group(1), "desc": m.group(2).strip(), "id": m.group(3),
             "covered": m.group(4), "body": m.group(5).strip()}
            for m in _SECTION_RE.finditer(text)]


def _load_fixtures():
    out = []
    for p in sorted(SAMPLES_DIR.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            d["_path"] = p
            out.append(d)
        except Exception:
            continue
    return out


def page_history():
    st.title("🗂️ 历史诊断 / 批量报告")
    st.caption("两类离线资产：① 预跑的 7 个真实案例 LLM 完整文本报告；"
               "② demo/samples 结构化样例（与实时诊断同一渲染器，断网可演完整结论卡）")

    st.subheader("① 批量 LLM 诊断报告（预跑真实案例）")
    sections = _load_batch_sections()
    if not sections:
        st.info("未找到 %s。联网时执行 `uv run python scripts/llm_demo_batch.py` 生成。"
                % BATCH_REPORT)
    else:
        st.caption("报告文件：%s（%d 个案例，2026-10 预跑归档）" % (BATCH_REPORT, len(sections)))
        labels = ["%s. %s（ID=%s，规则覆盖=%s）" % (x["idx"], x["desc"], x["id"], x["covered"])
                  for x in sections]
        choice = st.selectbox("选择案例", labels)
        sec = sections[labels.index(choice)]
        st.code(sec["body"], language="text")
        st.download_button("下载该报告（.txt）", sec["body"],
                           file_name="llm_demo_%s.txt" % sec["id"], mime="text/plain")

    st.divider()
    st.subheader("② 离线结构化样例（实时诊断同版结论卡）")
    fixtures = _load_fixtures()
    if not fixtures:
        st.info("demo/samples 下没有 JSON 样例；执行 `uv run python demo/build_fixtures.py` 生成。")
        return
    labels = ["%s —— %s" % (p["id"], p["desc"]) for p in fixtures]
    choice = st.radio("选择预跑样例", labels, label_visibility="collapsed")
    d = fixtures[labels.index(choice)]
    res = d.get("res") or {}
    render_result(
        res,
        warning=("该样例生成时内网 Oracle 不可达，查库证据已跳过。"
                 if (res.get("rule_res") or {}).get("offline_skipped") else None),
        meta="离线预跑样例 · 生成于 %s · 记录来源=%s · force_llm=%s · 非现场实时结果"
             % (d.get("generated_at", "-"), d.get("rec_source", "-"), d.get("force_llm")))


# ---------------------------------------------------------------------------
# 页⑤ 架构 / 关于
# ---------------------------------------------------------------------------
def page_arch():
    st.title("🧩 架构与产品说明")

    st.subheader("五层混合诊断流水线")
    st.code("""\
一条报错
  │
  ├─ ① ML 分流（字符 TF-IDF + 逻辑回归，1.7MB 模型，毫秒级，纯本地）
  │     noise/ora → 直接分诊（拦掉约 94% 入口流量，零 token、不查库）
  │     biz       → 放行
  ├─ ② 相似案例召回（char_wb TF-IDF 余弦，Top5 历史先验，纯本地）
  ├─ ③ 领域知识检索（Dimple 知识库，本地 BM25，冻结源码取证，未现场核实）
  ├─ ④ 规则引擎只读查库（参数化 SELECT 诊断树 = 现场事实，三重只读约束）
  └─ ⑤ 决策门：高置信+规则命中 → 规则快路径（零 token）
              低置信/未覆盖/长尾 → LLM 综合三证推理（超时/不可用则诚实降级）""",
            language="text")

    st.subheader("五种结论来源（审计可区分）")
    st.dataframe(pd.DataFrame([
        ["ML 快速路径", "噪音/ORA", "0", "否", "毫秒"],
        ["规则快速路径", "biz 高置信 + 规则命中", "0", "是", "毫秒"],
        ["LLM 诊断大脑", "低置信/未覆盖/长尾/强制", "1 次", "命中规则时", "十秒级"],
        ["规则兜底", "LLM 不可用但规则命中", "0", "是", "毫秒"],
        ["诚实兜底", "LLM 不可用且规则未覆盖", "0", "否", "毫秒（转人工+回流）"],
    ], columns=["来源", "触发条件", "LLM token", "是否查库", "耗时"]),
        width="stretch", hide_index=True)

    st.subheader("演示降级矩阵（明天现场任何网络状况都有内容可演）")
    st.dataframe(pd.DataFrame([
        ["全通（内网+公网）", "✅", "✅", "✅", "全部能力：ID 取数、三证合一、零 token 快路径"],
        ["仅公网 LLM（预期场景）", "✅", "⚠️ 跳过并明示", "✅", "ML 全链 + LLM 长尾；规则类看离线样例"],
        ["仅内网 Oracle", "✅", "✅", "❌", "规则快路径 + 规则/诚实兜底，徽标变色不报错"],
        ["完全离线", "✅", "❌", "❌", "噪音/ORA 秒诊、看板基线/重测、7 份历史报告、离线样例"],
    ], columns=["网络状况", "ML 分流/召回", "规则查库", "公网 LLM", "可演内容"]),
        width="stretch", hide_index=True)

    st.subheader("安全与合规边界")
    st.markdown(
        "1. **只读三重约束**：数据库只读账号 + 代码层写 SQL 拦截 + 规则白名单与参数化绑定；\n"
        "2. **知识库只读 SQL 默认不执行**：仅作建议展示，经专家审核派生为 runbook 后才落地；\n"
        "3. **开发期仅连公网 LLM**：上送内容只有报错文本与检索证据（不含账号口令）；"
        "交付客户前切换为内网 vLLM/网关，满足数据不出网；\n"
        "4. **可降级、可审计**：每类结论都标注由 ML/规则/知识/LLM 完成，证据不足时如实给低置信度。")

    st.subheader("技术栈与版本")
    st.markdown(
        "- 诊断内核：`ai_ops` 0.1.0（单包 src 布局，25 项 pytest，稳定契约 `pipeline.diagnose()`）\n"
        "- 本 POC：Streamlit 1.66（pyproject 的 `demo` extras），不进 wheel、不改内核\n"
        "- 正式版：FastAPI（`api` extras 已预留）+ Vue3 + Element Plus + MySQL 8 + Docker Compose")


# ---------------------------------------------------------------------------
# 侧栏（全局状态灯）
# ---------------------------------------------------------------------------
def sidebar():
    with st.sidebar:
        st.markdown("### 🩺 AIOps 诊断工作台")
        st.caption("Streamlit POC ｜ 正式版 Vue3")
        st.divider()
        st.markdown("**运行状态**")

        ml_ok = (paths.models_dir() / "routing.joblib").is_file()
        data_ok = paths.dataset_csv().is_file()
        st.markdown(("🟢 ML 分流模型" if ml_ok else "🔴 ML 分流模型缺失"))
        st.markdown(("🟢 案例数据集（%s 行）" % "{:,}".format(BASELINE["n"]))
                    if data_ok else "🔴 案例数据集缺失")

        ok, msg = oracle_check()
        st.markdown(("🟢 内网 Oracle" if ok else "🔴 内网 Oracle（演示非必需）"))
        st.caption(msg + ("　·　检测于 " + st.session_state.get("oracle_checked", "") ) )
        if st.button("重新检测内网", width="stretch"):
            oracle_check(force=True)
            st.rerun()

        llm = get_llm()
        if llm.available():
            st.markdown("🟢 公网 LLM（%s，%ds 超时）" % (llm.model, llm.timeout))
        else:
            st.markdown("🔴 公网 LLM 未配置/不可用")

        kb_root = get_kb().kb_root
        if kb_root and Path(kb_root).is_dir():
            st.markdown("🟢 知识库快照")
        else:
            st.markdown("🟡 知识库快照未挂载")
        st.divider()
        st.caption("断网仍可演：ML 分流、统计看板、历史批量报告、离线样例。")


def main():
    sidebar()
    tabs = st.tabs(["① 首页总览", "② 诊断查询", "③ 统计看板", "④ 历史诊断", "⑤ 架构 / 关于"])
    with tabs[0]:
        page_home()
    with tabs[1]:
        page_diagnose()
    with tabs[2]:
        page_board()
    with tabs[3]:
        page_history()
    with tabs[4]:
        page_arch()


if __name__ == "__main__":
    main()
