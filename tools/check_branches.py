# -*- coding: utf-8 -*-
"""验证诊断树的"查到/查不到"两个分支用真实数据。"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)
from engine.db import get_conn          # noqa: E402

conn = get_conn()
cur = conn.cursor()


def line(title, sql, p=None):
    print("\n## %s" % title)
    cur.execute(sql, p or {})
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    print("   %d 行: %s" % (len(rows), cols))
    for r in rows[:5]:
        print("   ", r)


# 持仓不足：成交编号前8位=20260827，客户持仓应有数据
line("持仓 20260827 Au(T+N1)（应查到，证明证据分支）",
     "SELECT CLEAR_DATE,CLIENT_ID,MEMBER_ID,CONTRACT_ID,SH_FLAG,BUY_QTY,SELL_QTY FROM CLEAR.TC_FTR_CLIENT_POSI_CLEAR WHERE CLEAR_DATE=:d AND MEMBER_ID=:m AND CLIENT_ID=:c AND CONTRACT_ID=:k",
     {"d": "20260827", "m": "016811", "c": "0000000168", "k": "Au(T+N1)"})

# 结算价：业务快照日 20260828，存在的合约 vs 不存在的期权合约
line("结算价 20260828 存在/不存在合约对照",
     "SELECT TRADE_DATE,CONTRACT_ID,CLEAR_PRICE FROM CLEAR.TC_CLEAR_PRICE WHERE TRADE_DATE=:d AND CONTRACT_ID IN ('Au(T+D)','Ag(T+D)','au2610C356')",
     {"d": "20260828"})

# 结算价表最新数据日期（旁证）
line("结算价表最新数据日期",
     "SELECT MAX(TRADE_DATE) FROM CLEAR.TC_CLEAR_PRICE")

# 递延费率 Ag(T+D) 20260828（应查到）
line("递延费率 Ag(T+D) 20260828（应查到）",
     "SELECT TRADE_DATE,CONTRACT_ID,MEMBER_ID,DEFER_FEE,PAY_FLAG FROM CLEAR.TC_DEFER_FEE_RATE WHERE TRADE_DATE=:d AND CONTRACT_ID=:k",
     {"d": "20260828", "k": "Ag(T+D)"})

# 一个确实不存在的合约结算价（用快照日，查不到=真缺失）
line("递延费率 Ag(T+D) 20260918（快照中无，查不到=缺失分支）",
     "SELECT TRADE_DATE,CONTRACT_ID,DEFER_FEE FROM CLEAR.TC_DEFER_FEE_RATE WHERE TRADE_DATE=:d AND CONTRACT_ID=:k",
     {"d": "20260918", "k": "Ag(T+D)"})

# 交易日历：20260828 / 20260918 是否交易日
line("交易日历 20260828 / 20260918",
     "SELECT TRADE_DATE,NOTE FROM INTERFACE.TP_EXCH_TRADE_DATE WHERE TRADE_DATE IN ('20260828','20260918')")

conn.close()
