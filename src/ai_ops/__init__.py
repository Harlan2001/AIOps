# -*- coding: utf-8 -*-
"""ai_ops —— 数据库业务报错智能诊断系统。

规则引擎确定性分流与查库取证 + Dimple 知识库领域知识 + LLM 长尾兜底（混合诊断）：
高频问题由规则毫秒级处理（零 token），仅长尾升级 LLM；全程对生产库只读、
可内网私有化部署、可降级、可审计。

对外稳定面：
- contract：diagnose(record) -> DiagnosisResult 数据契约（产品层只准依赖它）
- pipeline.diagnose：诊断编排（提交5 落地）
- cli.main：统一命令行入口
"""
__version__ = "0.1.0"

__all__ = ["__version__"]
