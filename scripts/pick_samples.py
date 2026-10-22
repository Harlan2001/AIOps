# -*- coding: utf-8 -*-
"""从数据集中挑选覆盖不同业务类型的代表性真实报错 ID（含完整参数、优先取有具体值的）。"""
import csv
from collections import defaultdict

from ai_ops import paths

DATA = str(paths.dataset_csv())

# 想覆盖的类型关键词（覆盖数据缺失/操作失败/规则校验/权限/持仓等不同大类）
WANT = [
    "结算价不存在", "递延费率不存在", "持仓不足", "库存量不足", "存续期变更失败",
    "修改[合约", "结算价", "费率", "不存在", "失败", "错误", "密码", "登录",
]


def main():
    with open(DATA, "r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    # 按 biz_type 聚合，挑“参数更具体（长度较长、不是纯模板）”的一条
    groups = defaultdict(list)
    for r in rows:
        if r["cls"] == "biz":
            groups[r["biz_type"]].append(r)

    # 按频次排序类型
    ranked = sorted(groups.items(), key=lambda kv: -len(kv[1]))

    picked = []
    seen_kw = set()
    # 先保证覆盖高频类型
    for bt, items in ranked[:25]:
        # 选文本里带具体合约/客户值（去掉模板后仍较长）的一条：含 [xxx=>yyy] 且 yy 非 ?
        cands = [x for x in items if "=>" in x["text"] and "?]" not in x["text"]]
        cand = cands[0] if cands else items[0]
        picked.append((bt, len(items), cand))

    print("共 %d 个业务类型，以下为 Top25 代表样本：\n" % len(groups))
    for i, (bt, cnt, r) in enumerate(picked, 1):
        print("%2d. [%-3d次] ID=%s  日期=%s  码=%s" % (i, cnt, r["id"], r["ldate"], r["errcode"]))
        print("    类型: %s" % bt)
        print("    文本: %s" % r["text"][:160])
        print()


if __name__ == "__main__":
    main()
