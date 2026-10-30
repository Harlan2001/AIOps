# -*- coding: utf-8 -*-
"""错误表报错覆盖率统计（GaussDB）。

对 7 张错误表：
  1. 数据库侧按报错文本 GROUP BY 取 TOP（本地归一化骨架后再聚合）
  2. 对照 errors.yaml 现有 runbook 关键词判定是否覆盖
  3. 输出每张表覆盖率、未覆盖高频骨架（= 待补 runbook 的优先级）
"""
import sys
from collections import defaultdict

import yaml

sys.path.insert(0, r"D:\document\yunwei\dimple\AIOps\src")
from ai_ops.engine.db import query
from ai_ops.engine.error_records import SOURCES, SCHEMA
from ai_ops.engine.parser import normalize_skeleton

RULES = r"D:\document\yunwei\dimple\AIOps\src\ai_ops\assets\rules\errors.yaml"
with open(RULES, "r", encoding="utf-8") as f:
    rules = yaml.safe_load(f)
KW = [(t["id"], t.get("keywords", [])) for t in rules["types"]]

NOISE_RULES = r"D:\document\yunwei\dimple\AIOps\src\ai_ops\assets\rules\noise_rules.yaml"
with open(NOISE_RULES, "r", encoding="utf-8") as f:
    noise_rules = yaml.safe_load(f)
NOISE_KW = list(noise_rules.get("noise_contains", []))


def covered(skeleton):
    """对齐引擎真实行为：先业务报错词（runbook 关键词），再噪音词。

    返回 (type_id 或 None, kind)：kind 为 "rule"（规则覆盖）/ "noise"（噪音过滤）/"miss"。
    """
    for tid, kws in KW:
        if any(k in skeleton for k in kws):
            return tid, "rule"
    if any(k in skeleton for k in NOISE_KW):
        return "__noise__", "noise"
    return None, "miss"


print("=" * 100)
grand_total = 0
grand_cov = 0
grand_noise = 0
uncovered = defaultdict(int)
for sid, src in SOURCES.items():
    table = "%s.%s" % (SCHEMA, src.his)
    text = src.text_col
    _, r = query("SELECT COUNT(*) FROM %s WHERE %s IS NOT NULL" % (table, text))
    total = r[0][0]
    sql = ("SELECT %s, COUNT(*) AS c FROM %s WHERE %s IS NOT NULL "
           "GROUP BY %s ORDER BY c DESC LIMIT 200") % (text, table, text, text)
    _, rows = query(sql)
    sk = defaultdict(int)
    for txt, c in rows:
        sk[normalize_skeleton(txt)] += c
    cov = 0
    noise = 0
    for skeleton, c in sk.items():
        tid, kind = covered(skeleton)
        if kind == "rule":
            cov += c
        elif kind == "noise":
            noise += c
        else:
            uncovered[(sid, skeleton)] += c
    grand_total += total
    grand_cov += cov
    grand_noise += noise
    pct = 100.0 * cov / total if total else 0
    print("[%s] %s  总 %d  TOP覆盖 %d (%.1f%%)  噪音过滤 %d  未覆盖 %d" % (
        sid, src.label, total, cov, pct, noise, total - cov - noise))
print("=" * 100)
print("合计：总 %d  已覆盖 %d  整体覆盖率 %.1f%%  噪音过滤 %d（不计故障）" % (
    grand_total, grand_cov, 100.0 * grand_cov / grand_total, grand_noise))
print("\n未覆盖高频骨架 TOP40（跨表，= 待补 runbook 优先级）：")
print("-" * 100)
for (sid, skeleton), c in sorted(uncovered.items(), key=lambda x: -x[1])[:40]:
    print("%-12s %8d  %s" % (sid, c, skeleton[:70]))
