# -*- coding: utf-8 -*-
"""纯规则诊断入口 + TLOG 取数。

- get_record_by_id：按 ID 从 ULOG.TLOG 取单条报错，返回标准化记录 dict；
- 本脚本可直接运行纯规则诊断（engine.rule_engine），不依赖 ML/LLM；
- hybrid_diagnose.py 复用这里的 get_record_by_id。
"""
import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from engine.db import get_conn            # noqa: E402
from engine.rule_engine import Engine     # noqa: E402
from engine.report import render          # noqa: E402


def get_record_by_id(rec_id):
    """按 ID 查询单条 TLOG，返回记录 dict；无结果返回 None。"""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT ID, TO_CHAR(LDATE,'YYYY-MM-DD HH24:MI:SS'), LLEVEL, ERRCODE,
                   LSECTION, LTEXTE, FUNC_NO
            FROM ULOG.TLOG WHERE ID = :rid
        """, {"rid": rec_id})
        row = cur.fetchone()
    finally:
        conn.close()
    if not row:
        return None
    _id, ldate, llevel, errcode, lsection, ltexte, func_no = row
    return {
        "id": _id,
        "ldate": ldate or "",
        "llevel": llevel,
        "errcode": int(errcode or 0),
        "func_no": func_no or "",
        "lsection": lsection or "",
        "text": (ltexte or "").strip(),
    }


def main():
    ap = argparse.ArgumentParser(description="纯规则诊断（不依赖 ML/LLM）")
    ap.add_argument("--id")
    ap.add_argument("--text")
    ap.add_argument("--ldate", default="")
    ap.add_argument("--errcode", type=int, default=0)
    args = ap.parse_args()

    if args.id:
        rec = get_record_by_id(int(args.id))
        if not rec:
            print("未找到 ID=%s 的日志" % args.id)
            sys.exit(1)
    elif args.text:
        rec = {"text": args.text, "ldate": args.ldate, "errcode": args.errcode,
               "lsection": "", "func_no": "", "llevel": None, "id": None}
    else:
        ap.print_help()
        sys.exit(2)

    eng = Engine()
    res = eng.diagnose(rec)
    print(render(res))
    eng.close()


if __name__ == "__main__":
    main()
