# -*- coding: utf-8 -*-
"""领域知识层适配：把 Dimple 知识库（dimple-knowledge-base）接入诊断管线。

设计要点：
- 纯本地 BM25 检索，离线、无网络 / 数据库 / API key / 向量库；
- 进程内用 importlib 加载知识库自带的 Knowledge 引擎（纯标准库），不启动额外服务；
- 任何加载 / 检索异常都静默降级（available()=False、diagnose()=None），绝不阻断主流程；
- 知识库只读 SQL 默认不自动执行（execute_kb_sql=false），仅作为建议文本与报告展示；
- 检索键使用中文症状（日志骨架），不使用 TLOG 数字错误码（两套编码体系不一致）。

接入位置：hybrid_diagnose 在 ML 判为 biz 后，与"相似案例召回""规则查库"并行检索本层。
"""
import importlib.util
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)

# 知识库诊断引擎（Knowledge 类）相对知识根的位置
_ENGINE_REL = os.path.join(
    "installation", "skills", "dimple-knowledge", "scripts", "kb.py")
# 引擎所在 scripts 目录（加入 sys.path，兼容其潜在同目录依赖）
_SCRIPTS_REL = os.path.join(
    "installation", "skills", "dimple-knowledge", "scripts")
_ENGINE_MODULE = "dimple_kb_engine"

_SQL_LIMIT = 400       # 单条只读 SQL 进入提示词的最大字符
_TXT_LIMIT = 200       # 单条文本截断


def _coerce(val):
    val = val.strip()
    if (val.startswith('"') and val.endswith('"')) or \
       (val.startswith("'") and val.endswith("'")):
        val = val[1:-1]
    low = val.lower()
    if low in ("true", "false"):
        return low == "true"
    if val == "":
        return ""
    try:
        return int(val)
    except ValueError:
        return val


def _load_simple_yaml(path):
    """极简 key: value 解析（kb.yaml 无嵌套结构）；PyYAML 缺失时兜底。"""
    cfg = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            key, _, val = line.partition(":")
            val = val.strip()
            if " #" in val:
                val = val.split(" #", 1)[0].rstrip()
            cfg[key.strip()] = _coerce(val)
    return cfg


def _load_config(path):
    if not os.path.isfile(path):
        return {}
    try:
        import yaml  # type: ignore
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data if isinstance(data, dict) else {}
    except Exception:
        try:
            return _load_simple_yaml(path)
        except Exception:
            return {}


def _clip(s, n=_TXT_LIMIT):
    s = str(s or "").replace("\n", " ").strip()
    return s if len(s) <= n else s[:n] + "…"


_PARAM_BLOCK_RE = re.compile(r"\[[^\]]*\]")
_CN_PHRASE_RE = re.compile(r"[\u4e00-\u9fff]{2,}")


def _clean_symptom(text):
    """从日志骨架提取中文症状短语：去掉参数块/占位符/英文/数字，
    保留中文业务描述，提升知识库 BM25 召回精度（不使用数字错误码）。"""
    if not text:
        return ""
    t = _PARAM_BLOCK_RE.sub(" ", text)
    t = t.replace("<", " ").replace(">", " ")
    return " ".join(_CN_PHRASE_RE.findall(t))[:80]


def _join(items, n=None):
    if isinstance(items, str):
        return items.strip()
    items = [str(x).strip() for x in (items or []) if str(x).strip()]
    if n:
        items = items[:n]
    return "；".join(items)


class KnowledgeClient:
    """领域知识检索客户端（可降级）。"""

    def __init__(self, cfg_path=None, kb_root=None, audience=None,
                 baseline=None, top=None, enabled=None):
        cfg_path = cfg_path or os.path.join(_ROOT, "config", "kb.yaml")
        cfg = _load_config(cfg_path)
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
                    "sql": _clip(q.get("sql", ""), _SQL_LIMIT),
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

    # ---------------- 给 LLM 的提示词块 ----------------
    @staticmethod
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
                L.append("  症状：%s" % _clip(c["symptom"], 160))
            if c["required_facts"]:
                L.append("  必须先确认的事实：" + _join(c["required_facts"], 14))
            if c["parameter_codes"]:
                L.append("  相关参数：" + "、".join(map(str, c["parameter_codes"])))
            for b in c["branches"]:
                L.append("  ◆ 候选根因分支：%s" % b["id"])
                if b["when_all"]:
                    L.append("      成立条件：" + _join(b["when_all"]))
                if b["exclude_when"]:
                    L.append("      反证/不适用：" + _join(b["exclude_when"]))
                if b["next_checks"]:
                    L.append("      下一步只读检查：" + _join(b["next_checks"]))
                for a in b["actions"]:
                    if a["title"]:
                        L.append("      候选处置：%s" % a["title"])
                    if a["allowed_when"]:
                        L.append("          允许条件：" + _join(a["allowed_when"]))
                    if a["forbidden_when"]:
                        L.append("          禁止条件：" + _join(a["forbidden_when"]))
                    if a["side_effects"]:
                        L.append("          副作用：" + _join(a["side_effects"]))
                    if a["verification"]:
                        L.append("          恢复验证：" + _join(a["verification"]))
                    if a["rollback_boundary"]:
                        L.append("          回退边界：" + _join(a["rollback_boundary"]))
            for q in c["readonly_queries"]:
                L.append("  只读SQL参考（%s，表 %s，方言 %s；需现场核对，禁止擅自执行）：%s"
                         % (q["purpose"] or "-", q["table"] or "-",
                            q["dialect"] or "-", q["sql"]))
                if q["interpretation"]:
                    L.append("      结果解释：%s" % _clip(q["interpretation"], 300))
            for lg in c["log_context"]:
                L.append("  日志锚点（%s/%s）：%s"
                         % (lg.get("logger", ""), lg.get("level", ""),
                            _clip(lg.get("template", ""), 160)))
        return "\n".join(L)

    # ---------------- 给 CLI 报告的知识卡文本 ----------------
    @staticmethod
    def to_report_lines(card):
        if not card or not card.get("cards"):
            return ["  （知识库未命中相关诊断材料）"]
        L = ["  知识版本 %s｜基线 %s｜相关父文档 %d 篇｜状态：冻结源码取证，未现场核实"
             % (card.get("knowledge_version", ""), card.get("baseline_id", ""),
                card.get("matched_document_count", 0))]
        for i, c in enumerate(card["cards"], 1):
            L.append("  %d. [%.1f] %s（%s）" % (i, c["score"], c["title"], c["document_id"]))
            L.append("       症状：%s" % (_clip(c["symptom"], 120) or "-"))
            for b in c["branches"][:3]:
                L.append("       · 根因分支 %s：%s"
                         % (b["id"], _clip(_join(b["when_all"], 3), 120)))
            if c["required_facts"]:
                L.append("       · 需先确认：%s" % _clip(_join(c["required_facts"], 6), 200))
            L.append("       · 取证材料：只读SQL模板 %d 条、日志锚点 %d 处（默认不自动执行）"
                     % (c["n_queries"], c["n_logs"]))
            if c["sources"]:
                s = c["sources"][0]
                L.append("       · 来源：%s %s %s"
                         % (s.get("repository", ""), s.get("path", ""), s.get("symbol", "")))
        return L
