# -*- coding: utf-8 -*-
"""历史报错回放：评估规则覆盖率（本地匹配，不查库）+ 抽样端到端诊断（查库）。"""
import os
import sys
from collections import Counter

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)

from ai_ops.engine.db import get_conn          # noqa: E402
from ai_ops.engine import parser as P          # noqa: E402
from ai_ops.engine.rule_engine import Engine   # noqa: E402
from ai_ops.engine.report import render        # noqa: E402


def main():
    sample_per_type = int(sys.argv[1]) if len(sys.argv) > 1 else 2

    conn = get_conn()
    cur = conn.cursor()
    cur.arraysize = 2000
    cur.execute("""
        SELECT ID, TO_CHAR(LDATE,'YYYY-MM-DD HH24:MI:SS'), LSECTION, LTEXTE, ERRCODE
        FROM ULOG.TLOG WHERE LLEVEL IN (20,30)
    """)
    rows = cur.fetchall()
    conn.close()

    eng = Engine()
    classes = Counter()
    matched = Counter()          # 命中类型的条数
    matched_by_type = {}         # type_id -> 收集样例
    unmatched_skel = Counter()

    for _id, dt, lsec, text, errcode in rows:
        text = (text or "").strip()
        cls = P.classify(text, errcode or 0)
        classes[cls] += 1
        if cls != "biz":
            continue
        tcfg, score = eng.match_type(text, errcode or 0)
        if tcfg:
            matched[tcfg["id"]] += 1
            matched_by_type.setdefault(tcfg["id"], []).append(
                {"id": _id, "ldate": dt, "lsection": lsec, "text": text, "errcode": errcode})
        else:
            unmatched_skel[P.normalize_skeleton(text)] += 1

    total_biz = classes["biz"]
    print("=" * 92)
    print("回放分类：noise=%d  ora=%d  biz=%d  other=%d" % (
        classes["noise"], classes["ora"], classes["biz"], classes["other"]))
    print("业务报错共 %d 条；当前已配置规则命中 %d 条，覆盖率 %.2f%%" % (
        total_biz, sum(matched.values()), 100.0 * sum(matched.values()) / total_biz))
    print("=" * 92)
    print("已配置规则覆盖：")
    for tid, c in matched.most_common():
        print("  %-28s %5d 条 (%.1f%%)" % (tid, c, 100.0 * c / total_biz))

    print("\n" + "=" * 92)
    print("未配置规则的业务报错 Top 15（下一步扩展目标）")
    print("=" * 92)
    for skel, c in unmatched_skel.most_common(15):
        print("  %5d  %s" % (c, skel))

    # 抽样端到端诊断（真正查库）
    print("\n" + "=" * 92)
    print("每类抽样 %d 条端到端诊断（真正执行只读 SQL）" % sample_per_type)
    print("=" * 92)
    for tid, samples in matched_by_type.items():
        for rec in samples[:sample_per_type]:
            res = eng.diagnose(rec)
            print(render(res))
    eng.close()


if __name__ == "__main__":
    main()
