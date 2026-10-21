# -*- coding: utf-8 -*-
"""引擎分类/匹配自测（不连库，纯逻辑）。"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)

from engine.rule_engine import Engine   # noqa: E402

eng = Engine()

CASES = [
    ("无需要发送的DAMS数据！", 0, "noise"),
    ("处理成功！", 0, "noise"),
    ("保证金询价业务结算处理完成!", 0, "noise"),
    ("SQLCODE:-1 SQLERRM:ORA-00001: unique constraint violated", 201908301, "ora"),
    ("[期权合约=>au2610C356]结算价不存在", 150302029, "settle_price_not_found"),
    ("[合约=>Ag(T+D)]递延费率不存在", 101022001, "defer_fee_not_found"),
    ("平仓错误,[会员->016811][客户->0000000168][合约->Au(T+N1)][买]持仓不足,尚缺<1>", 101028602, "position_not_enough"),
    ("[交易员=>trader1]库存量不足，不允许分配", 101028602, "biz_unmatched"),  # 不应误判持仓
    ("系统不存在该条记录,存续期变更失败", 100007602, "biz_unmatched"),       # 尚未配规则
]

print("=" * 80)
ok = True
for text, code, expect in CASES:
    cls = eng._classify(text, code)
    if cls == "biz":
        t, score = eng.match_type(text, code)
        got = t["id"] if t else "biz_unmatched"
    else:
        got = cls
    flag = "OK " if got == expect else "FAIL"
    if got != expect:
        ok = False
    print("[%s] 期望=%-24s 实际=%-24s | %s" % (flag, expect, got, text[:40]))
print("=" * 80)
print("全部通过" if ok else "存在失败项")
eng.close()
