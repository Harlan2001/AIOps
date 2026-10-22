# -*- coding: utf-8 -*-
"""兼容垫片（提交8 删除）：逻辑已迁入 ai_ops.pipeline / ai_ops.reporting，
入口统一为 `ai-ops`（或 `uv run ai-ops`）。

仍保留 diagnose / render 符号，供尚未迁移的工具脚本引用。
"""
from ai_ops.cli import main
from ai_ops.pipeline import diagnose
from ai_ops.reporting import render_hybrid as render

if __name__ == "__main__":
    main()
