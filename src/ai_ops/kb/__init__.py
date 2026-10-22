# -*- coding: utf-8 -*-
"""领域知识层（Dimple 知识库 dimple-knowledge-base）适配。

把知识库内置的运维诊断能力（Knowledge.diagnose）接入诊断管线，
为 LLM / 规则提供"权威机制与处置手册"证据：候选根因分支、成立/反证条件、
只读 SQL 模板、日志锚点、处置边界与恢复验证。
"""
from .client import KnowledgeClient

__all__ = ["KnowledgeClient"]
