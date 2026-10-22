# -*- coding: utf-8 -*-
"""统一命令行入口（提交2 为桥接版：转发根脚本；提交5 替换为正式实现）。"""
import sys

from . import paths


def main(argv=None):
    # 迁移期：可运行代码仍在仓库根（扁平结构），桥接到旧入口
    if paths.REPO_ROOT and str(paths.REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(paths.REPO_ROOT))
    import hybrid_diagnose
    if argv is not None:
        sys.argv = ["ai-ops"] + list(argv)
    hybrid_diagnose.main()
