# -*- coding: utf-8 -*-
"""领域知识层（Dimple KB）独立自测：不依赖 ML / 数据 / LLM。

    uv run python -m ai_ops.ops.kb_selftest
"""
import sys

from ai_ops import evidence
from ai_ops.kb.client import KnowledgeClient

CASES = ["持仓不足", "结算价不存在", "递延费率不存在", "用户名或密码错误"]


def main():
    print("=" * 88)
    print("KB 领域知识层 独立自测")
    print("=" * 88)
    kb = KnowledgeClient()
    if not kb.available():
        print("[FAIL] 知识库不可用：%s" % kb.engine_error())
        print("       请检查 config/kb.yaml 的 kb_root 是否指向含 manifest.json 的知识根。")
        sys.exit(1)
    print("[OK] 知识库已加载：%s" % kb.info())
    print("     execute_kb_sql = %s（False=只读 SQL 不自动执行，仅作建议）" % kb.execute_kb_sql)

    all_ok = True
    for symptom in CASES:
        card = kb.diagnose_card(symptom, top=2)
        print("-" * 88)
        if not card:
            print("[FAIL] 未命中：%s" % symptom)
            all_ok = False
            continue
        top = card["cards"][0]
        nb = sum(len(c["branches"]) for c in card["cards"])
        nq = sum(c["n_queries"] for c in card["cards"])
        nlog = sum(c["n_logs"] for c in card["cards"])
        print("症状：%s ｜ 命中父文档 %d 篇 ｜ 分支 %d ｜ 只读SQL %d ｜ 日志锚点 %d"
              % (symptom, card["matched_document_count"], nb, nq, nlog))
        print("  Top1：[%.1f] %s（%s）" % (top["score"], top["title"], top["document_id"]))
        if symptom == "持仓不足":
            ok = any(c["document_id"] == "business-position-decision" for c in card["cards"])
            print("  [断言] 持仓不足命中 business-position-decision：%s" % ("OK" if ok else "FAIL"))
            all_ok = all_ok and ok

    print("=" * 88)
    print("【三证合一·领域知识提示词块示例（持仓不足，前 22 行）】")
    card = kb.diagnose_card("持仓不足", top=1)
    for line in evidence.to_prompt_block(card).splitlines()[:22]:
        print(line)

    print("=" * 88)
    print("【降级测试】错误的 kb_root")
    bad = KnowledgeClient(kb_root="D:/__not_exist_kb__")
    print("  available() = %s" % bad.available())
    print("  diagnose_card() = %s" % bad.diagnose_card("持仓不足"))
    print("  错误信息：%s" % bad.engine_error())

    print("=" * 88)
    print("结果：%s" % ("全部通过" if all_ok else "存在未通过断言"))
    sys.exit(0 if all_ok else 2)


if __name__ == "__main__":
    main()
