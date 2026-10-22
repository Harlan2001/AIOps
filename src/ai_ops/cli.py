# -*- coding: utf-8 -*-
"""统一命令行入口（ai-ops）：混合诊断默认，--rule 走纯规则，--llm/--fast 控制决策门。"""
import argparse
import sys

from ai_ops import pipeline, reporting
from ai_ops.engine.rule_engine import Engine
from ai_ops.engine.tlog import get_record_by_id


def _build_parser():
    ap = argparse.ArgumentParser(prog="ai-ops", description="TLOG 智能诊断 CLI")
    ap.add_argument("--id", help="按 TLOG ID 取数诊断（需可连通 Oracle）")
    ap.add_argument("--text", help="直接传入报错文本诊断")
    ap.add_argument("--ldate", default="", help="--text 模式下的日志时间")
    ap.add_argument("--errcode", type=int, default=0, help="--text 模式下的错误码")
    ap.add_argument("--llm", action="store_true", help="强制走 LLM")
    ap.add_argument("--fast", action="store_true", help="强制规则快速路径（不调 LLM）")
    ap.add_argument("--rule", action="store_true", help="纯规则模式（不依赖 ML/LLM）")
    return ap


def _resolve_record(args):
    if args.id:
        rec = get_record_by_id(int(args.id))
        if not rec:
            print("未找到 ID=%s 的日志" % args.id)
            sys.exit(1)
        return rec
    if args.text:
        return {"text": args.text, "ldate": args.ldate, "errcode": args.errcode,
                "lsection": "", "func_no": "", "llevel": None, "id": None}
    return None


def main(argv=None):
    ap = _build_parser()
    args = ap.parse_args(argv)
    rec = _resolve_record(args)
    if rec is None:
        ap.print_help()
        sys.exit(2)

    if args.rule:
        eng = Engine()
        try:
            print(reporting.render_rule(eng.diagnose(rec)))
        finally:
            eng.close()
        return

    res = pipeline.diagnose(rec, force_llm=args.llm, force_fast=args.fast)
    print(reporting.render_hybrid(res))
