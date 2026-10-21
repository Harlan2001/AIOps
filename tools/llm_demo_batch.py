# -*- coding: utf-8 -*-
"""批量演示：对 7 条覆盖不同大类的真实报错强制走 LLM 诊断，
结果同时打印到控制台，并写入 reports/llm_demo_result.txt。
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)

from diagnose import get_record_by_id   # noqa: E402
import hybrid_diagnose as hd            # noqa: E402

# (日志ID, 说明, 是否已建规则)
SAMPLES = [
    (3674173785, "期权合约结算价不存在（数据缺失·已建规则，看查库取证）", True),
    (587223,     "递延费率不存在 Ag(T+D)（数据缺失·已建规则，看查库取证）", True),
    (4206226273, "mAu(T+D) 买持仓不足尚缺2（持仓类·已建规则，看查库取证）", True),
    (493325942,  "交易员可用库存量不足（持仓近似·未建规则，看是否误判）", False),
    (3659328059, "修改期权合约 au2607C376 失败（操作失败·未建规则长尾）", False),
    (636445574,  "用户名或密码错误（权限登录·未建规则长尾）", False),
    (1486259385, "用户使用未注册 IP（安全类·未建规则长尾）", False),
]


def main():
    report_dir = os.path.join(_ROOT, "reports")
    os.makedirs(report_dir, exist_ok=True)
    chunks = []
    for i, (sid, desc, has_rule) in enumerate(SAMPLES, 1):
        print("\n\n[%d/%d] %s  (ID=%s) ..." % (i, len(SAMPLES), desc, sid), flush=True)
        rec = get_record_by_id(sid)
        if not rec:
            print("  未找到 ID=%s 的日志" % sid)
            continue
        res = hd.diagnose(rec, force_llm=True)
        text = hd.render(res)
        print(text, flush=True)
        chunks.append("\n\n" + "#" * 100
                      + "\n# %d. %s\n# 日志ID=%s  规则覆盖=%s\n"
                      % (i, desc, sid, "是" if has_rule else "否") + "#" * 100 + "\n" + text)

    out = os.path.join(report_dir, "llm_demo_result.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(chunks))
    print("\n\n全部完成，结果已写入：%s" % out, flush=True)


if __name__ == "__main__":
    main()
