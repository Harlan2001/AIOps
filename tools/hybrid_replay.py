# -*- coding: utf-8 -*-
"""全量回放：统计混合架构下各处理路径的流量与 LLM 调用占比。

路径：
  ML 快速路径   ：noise/ora，ML 直接分流，不查库、不调 LLM
  规则快速路径  ：biz 且 ML 高置信 且 命中确定性规则，只读查库出结论，零 token
  LLM 诊断      ：低置信 / 规则未覆盖 / 口语化长尾，交给 LLM
另给出"规则补齐 Top30 后"的预估 LLM 调用率（数据飞轮/规则扩展的降本趋势）。
"""
import csv
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)

from ml.router import Router                 # noqa: E402
from ai_ops.engine.rule_engine import Engine        # noqa: E402

DATA = os.path.join(_ROOT, "data", "ml", "dataset.csv")


def main():
    with open(DATA, "r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    texts = [r["text"] for r in rows]
    N = len(rows)

    router = Router()
    th = router.threshold
    # 一级分流（批量）
    p1 = router.cls_route.predict_proba(texts)
    lab1 = router.cls_route.classes_[p1.argmax(axis=1)]
    conf1 = p1.max(axis=1)

    eng = Engine()
    n_ml_fast = 0
    biz_rows = []
    for i, lab in enumerate(lab1):
        if lab in ("noise", "ora"):
            n_ml_fast += 1
        elif lab == "biz":
            biz_rows.append((i, rows[i], conf1[i]))

    # 二级类型路由（批量，仅 biz）
    bx = [rows[i]["text"] for i, _, _ in biz_rows]
    p2 = router.cls_biz.predict_proba(bx)
    lab2 = router.cls_biz.classes_[p2.argmax(axis=1)]
    conf2 = p2.max(axis=1)

    cur_rule_fast = 0      # 当前规则(3类) + 高置信
    cur_llm = 0
    fut_rule_fast = 0      # 未来规则(Top30显式类) + 高置信
    fut_llm = 0
    low_conf = 0
    for k, (i, rec, _c) in enumerate(biz_rows):
        text = rec["text"]
        errcode = int(rec["errcode"] or 0)
        high = conf2[k] >= th
        if not high:
            low_conf += 1
        tcfg, _ = eng.match_type(text, errcode)
        cur_rule_hit = tcfg is not None
        fut_rule_hit = lab2[k] != "other_biz"
        if high and cur_rule_hit:
            cur_rule_fast += 1
        else:
            cur_llm += 1
        if high and fut_rule_hit:
            fut_rule_fast += 1
        else:
            fut_llm += 1

    B = len(biz_rows)
    print("=" * 90)
    print("混合架构全量分流测算（共 %d 条 FATAL/ERROR，置信度阈值 %.2f）" % (N, th))
    print("=" * 90)
    print("【ML 快速路径】噪音/ORA，ML 直接分流，零 token：%d 条，占总量 %.2f%%"
          % (n_ml_fast, 100.0 * n_ml_fast / N))
    print("业务报错：%d 条，占 %.2f%%" % (B, 100.0 * B / N))
    print("-" * 90)
    print("【当前：已建 3 类规则】")
    print("  规则快速路径（高置信+规则命中，零 token）：%d 条，占业务 %.2f%% / 总量 %.2f%%"
          % (cur_rule_fast, 100.0 * cur_rule_fast / B, 100.0 * cur_rule_fast / N))
    print("  需调用 LLM（低置信/未覆盖/长尾）        ：%d 条，占业务 %.2f%% / 总量 %.2f%%"
          % (cur_llm, 100.0 * cur_llm / B, 100.0 * cur_llm / N))
    print("  其中类型低置信（<%.2f）：%d 条" % (th, low_conf))
    print("-" * 90)
    print("【未来：规则补齐 Top30（覆盖业务 93.5%）】")
    print("  规则快速路径（高置信+规则命中，零 token）：%d 条，占业务 %.2f%% / 总量 %.2f%%"
          % (fut_rule_fast, 100.0 * fut_rule_fast / B, 100.0 * fut_rule_fast / N))
    print("  需调用 LLM（长尾/低置信）               ：%d 条，占业务 %.2f%% / 总量 %.2f%%"
          % (fut_llm, 100.0 * fut_llm / B, 100.0 * fut_llm / N))
    print("=" * 90)
    print("结论：ML 已在入口拦掉 %.2f%% 流量；规则补齐后，仅 %.2f%% 的总流量需要真正调用 LLM。"
          % (100.0 * n_ml_fast / N, 100.0 * fut_llm / N))
    eng.close()


if __name__ == "__main__":
    main()
