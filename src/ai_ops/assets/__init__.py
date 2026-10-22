# -*- coding: utf-8 -*-
"""随包发布的非代码资产（规则包等）。

资产随模块树进入 wheel（uv_build 自动递归打包，无需 MANIFEST.in），
git 可 diff、可 code review；加载与外挂覆盖逻辑见 ai_ops.rules_store。
"""
