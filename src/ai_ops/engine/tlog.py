# -*- coding: utf-8 -*-
"""TLOG 取数：按 ID 从 ULOG.TLOG 取单条报错，标准化为诊断记录 dict。"""
from ai_ops.engine.db import get_conn


def get_record_by_id(rec_id):
    """按 ID 查询单条 TLOG，返回记录 dict；无结果返回 None。"""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT ID, TO_CHAR(LDATE,'YYYY-MM-DD HH24:MI:SS'), LLEVEL, ERRCODE,
                   LSECTION, LTEXTE, FUNC_NO
            FROM ULOG.TLOG WHERE ID = :rid
        """, {"rid": rec_id})
        row = cur.fetchone()
    finally:
        conn.close()
    if not row:
        return None
    _id, ldate, llevel, errcode, lsection, ltexte, func_no = row
    return {
        "id": _id,
        "ldate": ldate or "",
        "llevel": llevel,
        "errcode": int(errcode or 0),
        "func_no": func_no or "",
        "lsection": lsection or "",
        "text": (ltexte or "").strip(),
    }
