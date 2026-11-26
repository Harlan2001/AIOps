# -*- coding: utf-8 -*-
"""引擎分类/类型匹配自测（不连库，纯逻辑），由 tools/selfcheck.py 迁入。"""
import pytest

from ai_ops.engine.rule_engine import Engine

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
    ("事中风控告警已恢复", 0, "noise"),  # 恢复通知优先于全局“告警”错误词
    ("告警处理成功", 0, "noise"),
    ("告警已经恢复", 0, "noise"),
    ("告警已恢复，但交易失败", 0, "biz_unmatched"),  # 同时有真实错误词仍按业务错误
]


@pytest.fixture(scope="module")
def eng():
    e = Engine()
    yield e
    e.close()


@pytest.mark.parametrize("text,errcode,expect", CASES)
def test_classify_and_match(eng, text, errcode, expect):
    cls = eng._classify(text, errcode)
    if cls == "biz":
        t, _score = eng.match_type(text, errcode)
        got = t["id"] if t else "biz_unmatched"
    else:
        got = cls
    assert got == expect


def test_iquant_closed_status_is_not_recovered_noise(eng):
    # “已处理”是 iQuant 闭环事件状态，不应当作“告警已恢复”噪音吞掉。
    assert eng._classify("事中风控告警：测试，事件状态 已处理", 0) == "biz"
