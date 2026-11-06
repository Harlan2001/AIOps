# -*- coding: utf-8 -*-
"""领域知识层适配：把 Dimple 知识库（dimple-knowledge-base）接入诊断管线。

设计要点：
- 纯本地 BM25 检索，离线、无网络 / 数据库 / API key / 向量库；
- 进程内用 importlib 加载知识库自带的 Knowledge 引擎（纯标准库），不启动额外服务；
- 任何加载 / 检索异常都静默降级（available()=False、diagnose()=None），绝不阻断主流程；
- 知识库只读 SQL 默认不自动执行（execute_kb_sql=false），仅作为建议文本与报告展示；
- 检索键使用中文症状（日志骨架），不使用 TLOG 数字错误码（两套编码体系不一致）。

接入位置：pipeline 在规则引擎识别业务报错后，与"规则查库取证"并行检索本层。
配置优先级：默认值 < config/kb.yaml < AIOPS_KB_* 环境变量 < 显式构造参数。
"""
import importlib.util
import os
import re
import sys

from ai_ops import evidence
from ai_ops.config import load_config

# 知识库诊断引擎（Knowledge 类）相对知识根的位置
_ENGINE_REL = os.path.join(
    "installation", "skills", "dimple-knowledge", "scripts", "kb.py")
# 引擎所在 scripts 目录（加入 sys.path，兼容其潜在同目录依赖）
_SCRIPTS_REL = os.path.join(
    "installation", "skills", "dimple-knowledge", "scripts")
_ENGINE_MODULE = "dimple_kb_engine"

_SQL_LIMIT = 400       # 单条只读 SQL 进入提示词的最大字符

_PARAM_BLOCK_RE = re.compile(r"\[[^\]]*\]")
_CN_PHRASE_RE = re.compile(r"[一-鿿]{2,}")


def _clean_symptom(text):
    """从日志骨架提取中文症状短语：去掉参数块/占位符/英文/数字，
    保留中文业务描述，提升知识库 BM25 召回精度（不使用数字错误码）。"""
    if not text:
        return ""
    t = _PARAM_BLOCK_RE.sub(" ", text)
    t = t.replace("<", " ").replace(">", " ")
    return " ".join(_CN_PHRASE_RE.findall(t))[:80]


class KnowledgeClient:
    """领域知识检索客户端（可降级）。"""

    def __init__(self, kb_root=None, audience=None,
                 baseline=None, top=None, enabled=None):
        cfg = load_config("kb")
        self.enabled = enabled if enabled is not None else bool(cfg.get("enabled", True))
        self.kb_root = kb_root or cfg.get("kb_root", "") or ""
        self.audience = audience if audience is not None else cfg.get("audience", "internal")
        self.baseline_cfg = baseline if baseline is not None else cfg.get("baseline", "")
        self.top = int(top or cfg.get("top", 3) or 3)
        self.execute_kb_sql = bool(cfg.get("execute_kb_sql", False))
        self._engine = None
        self._engine_error = None
        self._info = None

    # ---------------- 引擎加载（懒加载、容错） ----------------
    def _load_engine(self):
        if self._engine is not None:
            return self._engine
        if not self.enabled:
            self._engine_error = "kb.enabled=false（知识库检索已关闭）"
            return None
        if not self.kb_root or not os.path.isdir(self.kb_root):
            self._engine_error = "知识库目录不存在：%s" % self.kb_root
            return None
        engine_py = os.path.join(self.kb_root, _ENGINE_REL)
        scripts_dir = os.path.join(self.kb_root, _SCRIPTS_REL)
        if not os.path.isfile(engine_py):
            self._engine_error = "未找到知识库引擎：%s" % engine_py
            return None
        try:
            if scripts_dir not in sys.path:
                sys.path.insert(0, scripts_dir)
            spec = importlib.util.spec_from_file_location(_ENGINE_MODULE, engine_py)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            kn = mod.Knowledge(self.kb_root)
            self._engine = kn
            self._info = {
                "knowledge_version": kn.manifest.get("knowledge_version", ""),
                "baseline_id": kn.baseline,
                "projection_audience": kn.audience,
            }
            return kn
        except Exception as e:
            self._engine_error = "知识库加载失败：%s: %s" % (type(e).__name__, e)
            return None

    def available(self):
        return self._load_engine() is not None

    def engine_error(self):
        self._load_engine()
        return self._engine_error

    def info(self):
        self._load_engine()
        return dict(self._info or {})

    # ---------------- 门禁 / 范围 ----------------
    def _scope(self, kn):
        aud = str(self.audience or "internal").strip()
        include_internal = False
        if aud == "internal":
            customer = "common"
            include_internal = True
        elif aud in ("", "common"):
            customer = "common"
        else:
            customer = aud
        bcfg = str(self.baseline_cfg).strip()
        if bcfg.lower() == "unknown":
            return "unknown", "unknown", False
        if not bcfg:
            return kn.baseline, customer, include_internal
        return bcfg, customer, include_internal

    # ---------------- 原始诊断检索 ----------------
    def diagnose_raw(self, symptom, table=None, top=None):
        """返回知识库原始 diagnose dict；不可用 / 异常返回 None。"""
        kn = self._load_engine()
        if kn is None:
            return None
        symptom = (symptom or "").strip()
        if not symptom:
            return None
        query = _clean_symptom(symptom) or symptom
        baseline, customer, include_internal = self._scope(kn)
        try:
            return kn.diagnose(baseline, customer, query=query, table=table,
                               top=int(top or self.top),
                               include_internal=include_internal)
        except Exception as e:
            self._engine_error = "知识库诊断失败：%s: %s" % (type(e).__name__, e)
            return None

    # ---------------- 裁剪为诊断可用结构 ----------------
    def simplify(self, raw, max_matches=3, max_branches=4,
                 max_queries=3, max_logs=3, max_sources=2):
        """把知识库原始结果裁剪为结构化"知识卡"（控制提示词体积）。"""
        if not raw or not raw.get("matches"):
            return None
        cards = []
        for m in raw["matches"][:max_matches]:
            branches = []
            for b in (m.get("branches") or [])[:max_branches]:
                acts = []
                for a in (b.get("actions") or []):
                    acts.append({
                        "title": a.get("title", ""),
                        "allowed_when": a.get("allowed_when", []) or [],
                        "forbidden_when": a.get("forbidden_when", []) or [],
                        "side_effects": a.get("side_effects", []) or [],
                        "verification": a.get("verification", []) or [],
                        "rollback_boundary": a.get("rollback_boundary", []) or [],
                    })
                branches.append({
                    "id": b.get("id", ""),
                    "when_all": b.get("when_all", []) or [],
                    "exclude_when": b.get("exclude_when", []) or [],
                    "next_checks": b.get("next_checks", []) or [],
                    "actions": acts,
                })
            queries = []
            for q in (m.get("readonly_queries") or [])[:max_queries]:
                queries.append({
                    "purpose": q.get("purpose", ""),
                    "table": q.get("table", ""),
                    "dialect": q.get("dialect", ""),
                    "row_boundary": q.get("row_boundary", ""),
                    "interpretation": q.get("interpretation", ""),
                    "sql": evidence.clip(q.get("sql", ""), _SQL_LIMIT),
                    "executed": q.get("executed", False),
                })
            logs = []
            for lg in (m.get("log_context") or [])[:max_logs]:
                logs.append({
                    "caption": lg.get("caption", ""),
                    "level": lg.get("level", ""),
                    "logger": lg.get("logger", ""),
                    "template": lg.get("template", ""),
                    "search_anchor": lg.get("search_anchor", ""),
                })
            sources = []
            for s in (m.get("sources") or [])[:max_sources]:
                sources.append({
                    "repository": s.get("repository", ""),
                    "path": s.get("path", ""),
                    "symbol": s.get("symbol", ""),
                    "revision": s.get("revision") or s.get("operative_revision") or "",
                })
            cards.append({
                "score": round(float(m.get("score", 0.0)), 2),
                "document_id": m.get("document_id", ""),
                "title": m.get("title", ""),
                "symptom": m.get("symptom", ""),
                "domain": m.get("domain", ""),
                "required_facts": (m.get("required_facts") or [])[:14],
                "parameter_codes": m.get("parameter_codes") or [],
                "branches": branches,
                "readonly_queries": queries,
                "n_queries": len(m.get("readonly_queries") or []),
                "log_context": logs,
                "n_logs": len(m.get("log_context") or []),
                "sources": sources,
            })
        return {
            "knowledge_version": raw.get("knowledge_version", ""),
            "baseline_id": raw.get("baseline_id", ""),
            "context_gate": raw.get("context_gate", ""),
            "matched_document_count": raw.get("matched_document_count", 0),
            "runtime_verified": raw.get("runtime_verified", False),
            "execution_policy": raw.get("execution_policy", ""),
            "message": raw.get("message", ""),
            "cards": cards,
        }

    def diagnose_card(self, symptom, table=None, top=None):
        """便捷方法：直接返回裁剪后的知识卡 dict；未命中 / 不可用返回 None。"""
        raw = self.diagnose_raw(symptom, table=table, top=top)
        return self.simplify(raw) if raw else None
