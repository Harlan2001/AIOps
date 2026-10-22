# -*- coding: utf-8 -*-
"""从 ULOG.TLOG 历史报错自动生成"规则种子清单"（纯规则，零模型）。

输出：
  data/rule_seed.csv   业务报错类型种子（人工/LLM 蒸馏成 runbook 的输入）
  data/rule_seed.yaml  结构化版本
  data/ora_seed.csv    Oracle 技术错误种子（本期不做，备用）
  stdout               分类统计 / Top-N 覆盖率 / 待核对的 other 样例
"""
import os
import sys
import csv
from collections import Counter, defaultdict
from datetime import datetime

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)

from ai_ops.engine.db import get_conn           # noqa: E402
from ai_ops.engine import parser as P           # noqa: E402

DATA = os.path.join(_ROOT, "data")
os.makedirs(DATA, exist_ok=True)


def main():
    conn = get_conn()
    cur = conn.cursor()
    cur.arraysize = 2000
    cur.execute("""
        SELECT ID, TO_CHAR(LDATE,'YYYY-MM-DD HH24:MI:SS') AS DT, LSECTION, LTEXTE,
               ERRCODE, FUNC_NO
        FROM ULOG.TLOG WHERE LLEVEL IN (20,30)
    """)
    rows = cur.fetchall()
    conn.close()

    classes = Counter()
    biz = {}   # skeleton -> type dict
    ora = {}   # skeleton -> count
    noise = {}  # skeleton -> count
    other = {}

    for _id, dt, lsection, text, errcode, func_no in rows:
        text = (text or "").strip()
        cls = P.classify(text, errcode or 0)
        classes[cls] += 1
        skel = P.normalize_skeleton(text)

        if cls == "biz":
            t = biz.get(skel)
            if t is None:
                t = {
                    "skeleton": skel, "count": 0, "errcodes": Counter(),
                    "func_nos": Counter(), "modules": Counter(),
                    "params": Counter(), "samples": [], "first": dt, "last": dt,
                    "category": P.coarse_category(text),
                }
                biz[skel] = t
            t["count"] += 1
            if errcode:
                t["errcodes"][errcode] += 1
            if func_no:
                t["func_nos"][func_no] += 1
            loc = P.parse_lsection(lsection)
            if loc.get("module_label"):
                t["modules"][loc["module_label"]] += 1
            for f in P.extract_params(text):
                t["params"][f] += 1
            if dt < t["first"]:
                t["first"] = dt
            if dt > t["last"]:
                t["last"] = dt
            if len(t["samples"]) < 6:
                t["samples"].append({"dt": dt, "text": text})
        elif cls == "ora":
            ora[skel] = ora.get(skel, 0) + 1
        elif cls == "noise":
            noise[skel] = noise.get(skel, 0) + 1
        else:
            other[skel] = other.get(skel, 0) + 1

    # 排序、赋 type_id
    biz_sorted = sorted(biz.values(), key=lambda x: x["count"], reverse=True)
    total_biz = sum(t["count"] for t in biz_sorted)
    for i, t in enumerate(biz_sorted, 1):
        t["type_id"] = "biz_%03d" % i
        t["pct"] = round(100.0 * t["count"] / total_biz, 2)

    # ---------- 输出 CSV ----------
    csv_path = os.path.join(DATA, "rule_seed.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["type_id", "category", "count", "pct", "err_codes", "func_nos",
                    "modules", "param_fields", "first_seen", "last_seen", "skeleton", "sample"])
        for t in biz_sorted:
            w.writerow([
                t["type_id"], t["category"], t["count"], t["pct"],
                "; ".join("%s:%d" % (k, v) for k, v in t["errcodes"].most_common()),
                "; ".join(str(k) for k, _ in t["func_nos"].most_common(5)),
                "; ".join("%s:%d" % (k, v) for k, v in t["modules"].most_common(3)),
                "; ".join(t["params"].keys()),
                t["first"], t["last"], t["skeleton"],
                t["samples"][0]["text"] if t["samples"] else "",
            ])

    # ---------- 输出 YAML ----------
    yaml_doc = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_fatal_error": len(rows),
        "class_counts": dict(classes),
        "biz_type_count": len(biz_sorted),
        "biz_total": total_biz,
        "biz_types": [
            {
                "type_id": t["type_id"], "category": t["category"], "skeleton": t["skeleton"],
                "count": t["count"], "pct": t["pct"],
                "err_codes": [{"code": k, "count": v} for k, v in t["errcodes"].most_common()],
                "func_nos": [k for k, _ in t["func_nos"].most_common(5)],
                "modules": [k for k, _ in t["modules"].most_common(3)],
                "param_fields": list(t["params"].keys()),
                "first_seen": t["first"], "last_seen": t["last"],
                "samples": [s["text"] for s in t["samples"][:2]],
            }
            for t in biz_sorted
        ],
    }
    with open(os.path.join(DATA, "rule_seed.yaml"), "w", encoding="utf-8") as f:
        yaml.safe_dump(yaml_doc, f, allow_unicode=True, sort_keys=False, width=1000)

    # ---------- ORA 备用 ----------
    with open(os.path.join(DATA, "ora_seed.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["skeleton", "count"])
        for skel, c in sorted(ora.items(), key=lambda x: -x[1]):
            w.writerow([skel, c])

    # ---------- 噪音模式（用于 noise_rules）----------
    with open(os.path.join(DATA, "noise_seed.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["skeleton", "count"])
        for skel, c in sorted(noise.items(), key=lambda x: -x[1]):
            w.writerow([skel, c])

    # ---------- 控制台报告 ----------
    print("=" * 90)
    print("TLOG 报错分类（FATAL+ERROR 共 %d 条）" % len(rows))
    print("=" * 90)
    for k in ("noise", "ora", "biz", "other"):
        print("  %-6s %8d  %.2f%%" % (k, classes.get(k, 0), 100.0 * classes.get(k, 0) / len(rows)))

    print("\n" + "=" * 90)
    print("业务报错类型共 %d 种，合计 %d 条；粗分类分布：" % (len(biz_sorted), total_biz))
    print("=" * 90)
    catc = Counter()
    for t in biz_sorted:
        catc[t["category"]] += t["count"]
    for k, v in catc.most_common():
        print("  %-12s %6d  %.1f%%" % (k, v, 100.0 * v / total_biz))

    print("\n" + "=" * 90)
    print("Top-N 累计覆盖率（覆盖多少业务报错）")
    print("=" * 90)
    cum = 0
    for n in (10, 20, 30, 50, 100, len(biz_sorted)):
        c = sum(t["count"] for t in biz_sorted[:n])
        print("  Top %-3d : %6d 条  覆盖率 %.2f%%" % (n, c, 100.0 * c / total_biz))

    print("\n" + "=" * 90)
    print("Top 25 业务报错种子预览")
    print("=" * 90)
    for t in biz_sorted[:25]:
        print("\n[%s] %s  频次=%d (%.1f%%)  错误码=%s" % (
            t["type_id"], t["category"], t["count"], t["pct"],
            ",".join(str(k) for k in t["errcodes"]) or "无"))
        print("   骨架: %s" % t["skeleton"])
        print("   模块: %s  参数: %s" % (
            ",".join(t["modules"]) or "-", ",".join(t["params"]) or "-"))

    print("\n" + "=" * 90)
    print("noise 噪音模式 %d 种（已导出 noise_seed.csv，供过滤规则）" % len(noise))
    print("=" * 90)
    for skel, c in sorted(noise.items(), key=lambda x: -x[1])[:8]:
        print("  %6d  %s" % (c, skel))

    print("\n" + "=" * 90)
    print("other（真正未分类，共 %d 条 / %d 种）—— 需人工核对是否漏判" % (sum(other.values()), len(other)))
    print("=" * 90)
    for skel, c in sorted(other.items(), key=lambda x: -x[1]):
        print("  %6d  %s" % (c, skel))

    print("\n已生成：data/rule_seed.csv, data/rule_seed.yaml, data/ora_seed.csv, data/noise_seed.csv")


if __name__ == "__main__":
    main()
