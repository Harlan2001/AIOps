# -*- coding: utf-8 -*-
"""错误表报错覆盖率统计（GaussDB）。

对 7 张错误表：
  1. 数据库侧按报错文本 GROUP BY 取 TOP（本地归一化骨架后再聚合）
  2. 对照 errors.yaml 现有 runbook 关键词判定是否覆盖
  3. 输出每张表覆盖率、未覆盖高频骨架（= 待补 runbook 的优先级）

口径注：TOP_N 越大越接近全量（alarm 表 10.7M 条文本细长尾分布，
LIMIT 200 会把覆盖率低估到 46.9%，实际约 96%），默认 5000 覆盖 >99% 文本。

规则经 ai_ops.rules_store 加载，识别 AIOPS_RULES_DIR 外挂覆盖层；
import 本模块不再连库/执行，仅在显式运行（__main__）时统计。
"""
from collections import defaultdict

from ai_ops.engine.db import query
from ai_ops.engine.error_records import SOURCES, SCHEMA
from ai_ops.engine.parser import normalize_skeleton
from ai_ops.rules_store import load_registries

TOP_N = 5000


def _covered(skeleton, kw, noise_kw):
    """对齐引擎真实行为：先业务报错词（runbook 关键词），再噪音词。

    返回 (type_id 或 None, kind)：kind 为 "rule"（规则覆盖）/ "noise"（噪音过滤）/"miss"。
    """
    for tid, kws in kw:
        if any(k in skeleton for k in kws):
            return tid, "rule"
    if any(k in skeleton for k in noise_kw):
        return "__noise__", "noise"
    return None, "miss"


def main():
    # 规则经 rules_store 加载（含 AIOPS_RULES_DIR 覆盖层）
    types, noise_kw = load_registries()
    kw = [(t["id"], t.get("keywords", [])) for t in types]

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
               "GROUP BY %s ORDER BY c DESC LIMIT %d") % (text, table, text, text, TOP_N)
        _, rows = query(sql)
        sk = defaultdict(int)
        for txt, c in rows:
            sk[normalize_skeleton(txt)] += c
        cov = 0
        noise = 0
        for skeleton, c in sk.items():
            _tid, kind = _covered(skeleton, kw, noise_kw)
            if kind == "rule":
                cov += c
            elif kind == "noise":
                noise += c
            else:
                uncovered[(sid, skeleton)] += c
        sk_total = sum(sk.values())
        range_out = total - sk_total  # TOP_N 采样之外（长尾表需 SQL 全量 LIKE 复核）
        grand_total += total
        grand_cov += cov
        grand_noise += noise
        pct = 100.0 * cov / total if total else 0.0
        print("[%s] %s  总 %d  TOP覆盖 %d (%.1f%%)  噪音过滤 %d  未覆盖 %d  范围外 %d" % (
            sid, src.label, total, cov, pct, noise, sk_total - cov - noise, range_out))
    print("=" * 100)
    # 除零防护：grand_total 为 0（库不可达/无数据）时不做除法
    grand_pct = 100.0 * grand_cov / grand_total if grand_total else 0.0
    print("合计：总 %d  已覆盖 %d  整体覆盖率 %.1f%%  噪音过滤 %d（不计故障）" % (
        grand_total, grand_cov, grand_pct, grand_noise))
    print("\n未覆盖高频骨架 TOP40（跨表，= 待补 runbook 优先级）：")
    print("-" * 100)
    for (sid, skeleton), c in sorted(uncovered.items(), key=lambda x: -x[1])[:40]:
        print("%-12s %8d  %s" % (sid, c, skeleton[:70]))


if __name__ == "__main__":
    main()
