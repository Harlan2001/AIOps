# -*- coding: utf-8 -*-
"""诊断服务层（阶段 2·① / D1 方案 C）：把业务逻辑从 Streamlit 页面收敛到独立模块。

定位：
  - 纯 Python，零 UI 依赖（不 import streamlit）；
  - 页面（demo/app.py）、CLI 与 FastAPI 共用同一服务面；
  - 只做编排，不改诊断逻辑。

D1 方案 C 的两条诊断路径（响应统一为 contract.DiagnosisResult 形状）：
  - diagnose_rule_only：默认零 token，只跑规则引擎，不检索 KB、不调 LLM，kb_card=None；
  - diagnose_escalated：委托 ai_ops.pipeline.diagnose，规则命中仍零 token，
    仅长尾显式升级 LLM；部署未允许时由 API 依据 escalation_allowed 返回 409。

组件：Engine / KnowledgeClient / LLMClient 默认自建，可注入复用。
取数委托 ai_ops.engine.error_records（GaussDB 7 张错误历史表）。
"""
from datetime import datetime
from socket import create_connection
import time

from ai_ops import pipeline
from ai_ops.config import load_config
from ai_ops.engine import error_records as ER
from ai_ops.engine import parser as P
from ai_ops.engine.rule_engine import Engine
from ai_ops.kb.client import KnowledgeClient
from ai_ops.llm.client import LLMClient
from ai_ops.store import persist

# 真实记录演示（页①，从 GaussDB 错误表取数）
REAL_DEMOS = [
    ("演示① 敞口不够（GaussDB 真实记录）", "exposure",
     {"trade_date": "20250304", "trader_no": "trader",
      "local_no": "000000000001", "purpose_code": "ZY"}),
    ("演示③ 平仓数量不够（GaussDB 真实记录）", "close_posi",
     {"trade_date": "20250321", "trader_no": "trader9",
      "local_no": "000000000006", "purpose_code": "ZY"}),
    ("演示④ 策略资金不足（GaussDB 真实记录，最高频）", "fund",
     {"trade_date": "20250321", "trader_no": "trader1",
      "local_no": "000000240421", "purpose_code": "ZY"}),
]


def build_engine():
    return Engine()


def build_kb():
    return KnowledgeClient()


def build_llm():
    return LLMClient()


# 单请求批量取数/诊断的硬上限（B7：杜绝无 LIMIT 全量回放拖垮服务）
MAX_BATCH = 200


class DiagnosticService:
    """诊断服务：取数 → 诊断 → 证据增强；页面 / CLI / API 共用同一服务面。"""

    def __init__(self, eng=None, kb=None, llm=None):
        self.eng = eng if eng is not None else build_engine()
        self.kb = kb if kb is not None else build_kb()
        self.llm = llm if llm is not None else build_llm()

    # ---- 取数（委托 error_records，GaussDB 7 来源）----

    def sources(self):
        return ER.SOURCES

    def get_record(self, source, key):
        """按来源主键取单条错误记录；无结果返回 None。"""
        return ER.get_record(source, key)

    def list_records(self, source, date, limit=None):
        """按来源/日期取错误记录（仅文本非空）；limit 限制取数条数。"""
        return ER.list_records(source, date, limit=limit)

    def demo_record(self, key):
        """按演示 key 取对应真实错误记录（页①一键演示）。"""
        for _label, _key, d in REAL_DEMOS:
            if _key == key:
                return ER.get_record("ftr_err", d)
        return None

    # ---- D1 升级硬熔断（部署级允许位）----

    def escalation_allowed(self):
        """config/llm.yaml 的 allow_escalation（默认 false，私有化合规默认不允许升级）。"""
        cfg = load_config("llm")
        return bool(cfg.get("allow_escalation", False))

    # ---- 诊断：D1 两条路径，统一 DiagnosisResult 形状 ----

    @staticmethod
    def _base_envelope(rec, rule_res, kb_card, escalated):
        return {
            "text": rec.get("text", ""),
            "errcode": rec.get("errcode", 0),
            "ldate": rec.get("ldate", ""),
            "loc": pipeline._loc_str(P.parse_lsection(rec.get("lsection"))),
            "rule_res": rule_res,
            "kb_card": kb_card,
            "answer": None,
            "source": "",
            "escalated": escalated,
        }

    def _rule_only_core(self, rec):
        """默认路径：只跑规则引擎并适配为契约结构；不检索 KB、不调 LLM（零 token）。"""
        rule_res = self.eng.diagnose(rec)
        out = self._base_envelope(rec, rule_res, kb_card=None, escalated=False)
        cls = rule_res.get("class")
        if cls in ("noise", "ora"):
            out["answer"] = {"root": rule_res.get("verdict"),
                             "actions": [], "confidence": 1.0}
            out["source"] = "规则快速路径（噪音/技术错误，零 token）"
            return out
        if not rule_res.get("type"):
            # 未识别类型：无 runbook 取证，低置信度，结论为引擎兜底 verdict
            out["answer"] = {"root": rule_res.get("verdict"),
                             "actions": [], "confidence": pipeline.LOW_CONFIDENCE}
            out["source"] = "规则快速路径（未识别类型，零 token）"
            return out
        primary_ok = bool(rule_res.get("primary_evidence_ok"))
        confidence = 1.0 if primary_ok else pipeline.LOW_CONFIDENCE
        # 复用 pipeline 的 answer 构造（actions 重命名、secondary、evidence_note）
        out["answer"] = pipeline._rule_answer(rule_res, confidence)
        if primary_ok:
            out["source"] = "规则快速路径（纯规则，零 token）"
        else:
            out["source"] = "规则快速路径（纯规则，主检查无成功取证，已降置信度，零 token）"
        return out

    def _escalated_core(self, rec):
        """升级路径：委托 pipeline（共享 engine/kb/llm），返回契约结构并标 escalated=true。"""
        out = pipeline.diagnose(
            rec, eng=self.eng, kbcli=self.kb, llm=self.llm)
        out["escalated"] = True
        return out

    def diagnose_rule_only(self, rec, _ctx=None):
        """默认纯规则路径（带 best-effort 落库）。"""
        out = self._rule_only_core(rec)
        self._persist(rec, out, _ctx)
        return out

    def diagnose_escalated(self, rec, _ctx=None):
        """可选 LLM 升级路径（带 best-effort 落库）。"""
        out = self._escalated_core(rec)
        self._persist(rec, out, _ctx)
        return out

    def diagnose(self, rec):
        """兼容入口：等价于默认纯规则路径。"""
        return self.diagnose_rule_only(rec)

    def _persist(self, rec, out, ctx):
        """统一 best-effort 落库；落库失败由 persist 内部吞掉，不影响诊断。"""
        ctx = ctx or {}
        trigger_type = ctx.get("trigger_type") or "manual"
        batch_id = ctx.get("batch_id")
        is_error = isinstance(out, dict) and bool(out.get("_diagnose_error"))
        persist.persist_diagnosis(
            rec, out, trigger_type, batch_id=batch_id,
            diag_status="error" if is_error else "success",
            error_msg=out.get("_diagnose_error") if is_error else None)

    def diagnose_many(self, recs):
        """批量诊断（纯规则），返回 [(record, contract_result), ...]。"""
        ctx = {"trigger_type": "manual_batch"}
        return [(r, self.diagnose_rule_only(r, _ctx=ctx)) for r in recs]

    def diagnose_many_isolated(self, recs, escalate_flags=None, _ctx=None):
        """批量诊断（逐项隔离，B7/D1）：单条异常不拖垮整批。

        escalate_flags 为与 recs 对齐的 bool 序列，True 的条目走升级路径，
        其余纯规则；source+date 整表回放不传该参数，默认全部纯规则。
        诊断抛异常时第二项返回 {"_diagnose_error": "..."}，由 API 序列化。
        _ctx 提供 trigger_type/batch_id（巡检传 scheduled + 批次号）。
        """
        ctx = _ctx or {"trigger_type": "manual_batch"}
        out = []
        for i, r in enumerate(recs):
            do_escalate = bool(escalate_flags and escalate_flags[i])
            try:
                if do_escalate:
                    res = self.diagnose_escalated(r, _ctx=ctx)
                else:
                    res = self.diagnose_rule_only(r, _ctx=ctx)
            except Exception as e:
                res = {"_diagnose_error": "%s: %s" % (
                    type(e).__name__, str(e)[:200])}
                self._persist(r, res, ctx)
            out.append((r, res))
        return out

    # ---- 证据增强（KB 知识卡，仅升级路径使用；保留方法供页面显式调用）----

    def kb_card(self, text):
        """知识库机制卡；知识库不可用时返回 None（静默降级）。"""
        if not self.kb.available():
            return None
        return self.kb.diagnose_card(text)

    # ---- 环境预检 ----

    # GaussDB 探测缓存（N4）：避免每次 /healthz 都阻塞 1.5s
    _GAUSS_TTL = 30.0
    _GAUSS_CACHE = {"ts": -1.0, "data": None}

    @staticmethod
    def check_gauss(timeout=1.5, force=False):
        """GaussDB TCP 预检（host/port），返回 {ok, msg, checked}。

        结果按 _GAUSS_TTL 秒缓存；force=True 可强制重探。
        """
        now = time.monotonic()
        if not force and DiagnosticService._GAUSS_CACHE["data"] is not None \
                and now - DiagnosticService._GAUSS_CACHE["ts"] < DiagnosticService._GAUSS_TTL:
            return DiagnosticService._GAUSS_CACHE["data"]
        cfg = load_config("db")
        host, port = cfg.get("host"), int(cfg.get("port") or 0)
        try:
            with create_connection((host, port), timeout=timeout):
                ok = True
                msg = "%s:%s 可达（库 %s）" % (host, port, cfg.get("database"))
        except OSError as e:
            ok = False
            msg = "%s:%s 不可达（%s）" % (host, port, type(e).__name__)
        data = {"ok": ok, "msg": msg, "checked": datetime.now().strftime("%H:%M:%S")}
        DiagnosticService._GAUSS_CACHE["ts"] = now
        DiagnosticService._GAUSS_CACHE["data"] = data
        return data
