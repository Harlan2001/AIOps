# -*- coding: utf-8 -*-
"""兼容垫片（提交8 删除）：TLOG 取数已迁入 ai_ops.engine.tlog，
纯规则诊断入口统一为 `ai-ops --rule`。

仍保留 get_record_by_id 符号，供尚未迁移的工具脚本引用。
"""
import sys

from ai_ops.cli import main as _cli_main
from ai_ops.engine.tlog import get_record_by_id


def main():
    _cli_main(["--rule"] + sys.argv[1:])


if __name__ == "__main__":
    main()
