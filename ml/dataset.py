# -*- coding: utf-8 -*-
"""从 ULOG.TLOG 构建 ML 分流器训练数据集（落盘 CSV）。

两级标签：
  routing : noise / ora / biz / other      （一级分流）
  biz_type: biz 内部按骨架聚类的类型，Top-N 显式类，其余记为 other_biz（交给 LLM）
"""
import collections
import csv
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)

from ai_ops.engine.db import get_conn          # noqa: E402
from ai_ops.engine import parser as P          # noqa: E402

OUT_DIR = os.path.join(_ROOT, "data", "ml")
TOP_N = 30
FIELDS = ["id", "ldate", "llevel", "errcode", "func_no", "cls",
          "biz_type", "skeleton", "module", "deep_proc", "text", "lsection"]


def fetch_fatal_error():
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.arraysize = 2000
        cur.execute("""
            SELECT ID, LDATE, LLEVEL, ERRCODE, LSECTION, LTEXTE, FUNC_NO
            FROM ULOG.TLOG
            WHERE LLEVEL IN (20, 30)
            ORDER BY ID
        """)
        return cur.fetchall()
    finally:
        conn.close()


def build(top_n=TOP_N):
    rows = fetch_fatal_error()
    records = []
    type_counter = collections.Counter()
    cls_counter = collections.Counter()

    for _id, ldate, llevel, errcode, lsection, ltexte, func_no in rows:
        errcode = int(errcode or 0)
        text = ltexte or ""
        cls = P.classify(text, errcode)
        skel = P.normalize_skeleton(text)
        loc = P.parse_lsection(lsection or "")
        cls_counter[cls] += 1
        if cls == "biz":
            type_counter[skel] += 1
        records.append({
            "id": _id,
            "ldate": str(ldate),
            "llevel": llevel,
            "errcode": errcode,
            "func_no": func_no or "",
            "cls": cls,
            "biz_type": "",
            "skeleton": skel,
            "module": loc.get("module_label", ""),
            "deep_proc": loc.get("deep_proc", ""),
            "text": text,
            "lsection": lsection or "",
        })

    top_types = {s for s, _ in type_counter.most_common(top_n)}
    for rec in records:
        if rec["cls"] == "biz":
            rec["biz_type"] = rec["skeleton"] if rec["skeleton"] in top_types else "other_biz"

    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, "dataset.csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for rec in records:
            w.writerow(rec)

    print("=" * 80)
    print("已写出数据集：%s  共 %d 条" % (path, len(records)))
    print("-" * 80)
    print("一级分流标签分布：")
    for k, v in cls_counter.most_common():
        print("  %-6s %7d (%.2f%%)" % (k, v, 100.0 * v / len(records)))
    print("-" * 80)
    print("业务报错显式建模 Top%d 类，其余归 other_biz；Top%d 类样本：" % (top_n, top_n))
    cum = 0
    biz_total = sum(type_counter.values())
    for i, (s, c) in enumerate(type_counter.most_common(top_n), 1):
        cum += c
        print("  %3d. [%5d] %s" % (i, c, s[:70]))
    print("  Top%d 覆盖业务报错 %.2f%%（显式类合计 %d / biz %d）"
          % (top_n, 100.0 * cum / biz_total, cum, biz_total))
    print("=" * 80)
    return path


if __name__ == "__main__":
    build()
