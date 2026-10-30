# -*- coding: utf-8 -*-
"""统一命令行入口（ai-ops）：混合诊断默认，--rule 走纯规则，--llm/--fast 控制决策门。

GaussDB 版取数方式（无 TLOG）：
  --source 来源 --date 日期                诊断该来源当日全部错误（回放）
  --source 来源 --date 日期 --trader-no ..  按主键取单条
  --all-sources --date 日期                跨来源诊断当日全部错误
  --text "报错文本"                        直接传文本
默认查历史表，加 --today 查当日表。
"""
import argparse
import sys

from ai_ops import pipeline, reporting
from ai_ops.engine.rule_engine import Engine
from ai_ops.engine import error_records as ER

# 命令行参数名 -> 主键列名
_KEY_ARGS = [
    ("trader_no", "trader_no"),
    ("local_no", "local_no"),
    ("seq_no", "seq_no"),
    ("purpose", "purpose_code"),
    ("flow_code", "flow_code"),
    ("alarm_type", "alarm_type"),
    ("member", "member_id"),
]


def _build_parser():
    ap = argparse.ArgumentParser(prog="ai-ops", description="业务报错智能诊断 CLI（GaussDB）")
    ap.add_argument("--source", choices=list(ER.SOURCES), help="错误来源")
    ap.add_argument("--date", help="业务日期 YYYYMMDD")
    ap.add_argument("--today", action="store_true", help="查当日表（默认查历史表）")
    ap.add_argument("--all-sources", action="store_true", help="跨来源取当日全部错误")
    for argname, _col in _KEY_ARGS:
        ap.add_argument("--" + argname.replace("_", "-"), help="主键参数 %s" % argname)
    ap.add_argument("--text", help="直接传入报错文本诊断")
    ap.add_argument("--ldate", default="", help="--text 模式下的日志时间")
    ap.add_argument("--errcode", type=int, default=0, help="--text 模式下的错误码")
    ap.add_argument("--llm", action="store_true", help="强制走 LLM")
    ap.add_argument("--fast", action="store_true", help="强制规则快速路径（不调 LLM）")
    ap.add_argument("--rule", action="store_true", help="纯规则模式（不依赖 ML/LLM）")
    return ap


def _resolve_records(args):
    if args.text:
        return [{"text": args.text, "ldate": args.ldate, "errcode": args.errcode,
                 "lsection": "", "func_no": "", "llevel": None, "id": None}]
    if not args.date:
        return None
    history = not args.today
    if args.all_sources:
        return ER.list_by_date(args.date, history=history)
    if not args.source:
        return None

    key = {}
    for argname, col in _KEY_ARGS:
        val = getattr(args, argname)
        if val:
            key[col] = float(val) if col == "seq_no" else val
    if key:
        src = ER.SOURCES[args.source]
        key[src.date_col] = args.date
        rec = ER.get_record(args.source, key, history=history)
        return [rec] if rec else []
    return ER.list_records(args.source, args.date, history=history)


def main(argv=None):
    ap = _build_parser()
    args = ap.parse_args(argv)
    records = _resolve_records(args)
    if records is None:
        ap.print_help()
        sys.exit(2)
    if not records:
        print("未找到匹配的错误记录")
        sys.exit(1)

    for i, rec in enumerate(records):
        if len(records) > 1:
            print("\n########## 记录 %d/%d 来源=%s 主键=%s" %
                  (i + 1, len(records), rec.get("source"), rec.get("key")))
        if args.rule:
            eng = Engine()
            try:
                print(reporting.render_rule(eng.diagnose(rec)))
            finally:
                eng.close()
        else:
            res = pipeline.diagnose(rec, force_llm=args.llm, force_fast=args.fast)
            print(reporting.render_hybrid(res))
