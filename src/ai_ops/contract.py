# -*- coding: utf-8 -*-
"""诊断内核的稳定契约：diagnose(record) -> DiagnosisResult。

产品层（FastAPI / 调度 / worker / Streamlit）只允许依赖本契约与 ai_ops.pipeline，
不得反向要求内核感知接口、ORM 或前端。D1 方案 C 落地后，HTTP 侧有两条路径，
但响应统一为本文件定义的 DiagnosisResult 形状：
  - 默认纯规则：service.diagnose_rule_only 用轻量适配器把 Engine 结果映射成本结构，
    零 token、不检索 KB、不调 LLM；
  - 可选升级：service.diagnose_escalated 委托 pipeline.diagnose，仅显式 escalate 且
    部署允许（llm.allow_escalation）时才可能调用 LLM，运行时不可用则优雅降级。
Engine 内部 dict（如 action 字段）不得直接透传到产品层，重命名在适配器内完成。
真要独立发布内核时，沿本文件拆包即可。
"""
from __future__ import annotations

from typing import Any, List, Optional, TypedDict


class DiagnosisRecord(TypedDict, total=False):
    """标准化的一条报错输入（GaussDB 错误记录或粘贴文本）。"""
    id: Optional[int]
    text: str           # 报错原文
    errcode: int        # 数字错误码（不同场景复用，不能单独决定类型）
    ldate: str          # YYYY-MM-DD HH:MM:SS
    llevel: Optional[int]
    lsection: str       # 调用链原文（PKC_ 包 / SP_ 过程 / 行号）
    func_no: Optional[str]


class Evidence(TypedDict, total=False):
    id: str
    title: Optional[str]
    kind: str
    r: dict             # {"status": ok|missing_params, "cols": [...], "rows": [...]}


class Answer(TypedDict, total=False):
    root: str
    actions: List[str]
    confidence: float
    secondary: List[dict]
    evidence_note: str


class DiagnosisResult(TypedDict, total=False):
    """诊断管线的结构化输出；渲染层与 API 序列化均只消费本结构。"""
    text: str
    errcode: int
    ldate: str
    loc: str
    rule_res: Optional[dict]          # 规则引擎只读查库结果（含 Evidence 列表）
    kb_card: Optional[dict]           # Dimple 知识卡（机制证据）
    answer: Optional[Answer]
    source: str                       # 结论来源标注（可解释、可审计）


# 来源标注（报告逐步标注由规则/知识库/LLM 完成）
SOURCE_RULE_FAST = "规则快速路径（规则查库取证，零 token）"
SOURCE_LLM = "LLM 诊断大脑（规则识别 + KB 知识卡 + 规则取证）"
SOURCE_RULE_FALLBACK = "规则兜底（LLM 未配置/不可用，已按规则查库）"
SOURCE_GENERIC_FALLBACK = "兜底（LLM 未配置 + 规则未覆盖）"
