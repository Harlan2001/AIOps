# -*- coding: utf-8 -*-
"""用真实报错样本验证 runbook 候选只读 SQL（零模型）。"""
import re

from ai_ops.engine.db import get_conn
from ai_ops.engine import parser as P

CASES = {
    "结算价不存在": "%结算价不存在%",
    "递延费率不存在": "%递延费率不存在%",
    "持仓不足": "%持仓不足%",
}
_BIND_RE = re.compile(r":(\w+)")


def fetch_samples(cur, like, n=2):
    cur.execute("""
        SELECT ID, TO_CHAR(LDATE,'YYYY-MM-DD HH24:MI:SS') DT, LSECTION, LTEXTE, ERRCODE
        FROM ULOG.TLOG WHERE LLEVEL IN (20,30) AND LTEXTE LIKE :t
        ORDER BY LDATE DESC FETCH FIRST :n ROWS ONLY
    """, t=like, n=n)
    return cur.fetchall()


def run_sql(cur, name, sql, params):
    print("  -- %s" % name)
    print("     SQL: %s" % " ".join(sql.split()))
    need = set(_BIND_RE.findall(sql))
    b = {k: v for k, v in params.items() if k in need}
    missing = need - set(b)
    if missing:
        print("     !! 缺少绑定参数: %s" % missing)
        return
    try:
        cur.execute(sql, b)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        print("     结果 %d 行: %s" % (len(rows), cols))
        for r in rows[:3]:
            print("       ", r)
    except Exception as e:
        print("     !! SQL 错误:", e)


def main():
    conn = get_conn()
    cur = conn.cursor()

    for name, like in CASES.items():
        print("\n" + "#" * 100)
        print("# 案例：%s" % name)
        print("#" * 100)
        for _id, dt, lsec, text, errcode in fetch_samples(cur, like):
            print("\n>> 报错 ID=%s 时间=%s 错误码=%s" % (_id, dt, errcode))
            print("   文本: %s" % text)
            params = P.extract_params(text)
            loc = P.parse_lsection(lsec)
            trade_date = dt[:10].replace("-", "")
            print("   解析参数: %s" % params)
            print("   模块: %s . %s : %s" % (loc.get("deep_pkg"), loc.get("deep_proc"), loc.get("deep_line")))
            p = {"trade_date": trade_date,
                 "contract": params.get("合约") or params.get("期权合约"),
                 "member": params.get("会员"), "client": params.get("客户")}
            if "结算价不存在" in text:
                run_sql(cur, "交易日", "SELECT TRADE_DATE,NOTE FROM INTERFACE.TP_EXCH_TRADE_DATE WHERE TRADE_DATE=:trade_date", p)
                run_sql(cur, "结算价", "SELECT TRADE_DATE,CONTRACT_ID,CLEAR_PRICE,IF_MANUAL FROM CLEAR.TC_CLEAR_PRICE WHERE TRADE_DATE=:trade_date AND CONTRACT_ID=:contract", p)
            elif "递延费率不存在" in text:
                run_sql(cur, "交易日", "SELECT TRADE_DATE,NOTE FROM INTERFACE.TP_EXCH_TRADE_DATE WHERE TRADE_DATE=:trade_date", p)
                run_sql(cur, "递延费率", "SELECT TRADE_DATE,CONTRACT_ID,MEMBER_ID,DEFER_FEE,PAY_FLAG FROM CLEAR.TC_DEFER_FEE_RATE WHERE TRADE_DATE=:trade_date AND CONTRACT_ID=:contract", p)
            elif "持仓不足" in text:
                run_sql(cur, "客户持仓", "SELECT CLEAR_DATE,CLIENT_ID,MEMBER_ID,CONTRACT_ID,SH_FLAG,BUY_QTY,SELL_QTY FROM CLEAR.TC_FTR_CLIENT_POSI_CLEAR WHERE CLEAR_DATE=:trade_date AND MEMBER_ID=:member AND CLIENT_ID=:client AND CONTRACT_ID=:contract", p)
    conn.close()


if __name__ == "__main__":
    main()
