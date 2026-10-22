# -*- coding: utf-8 -*-
"""预跑离线演示样例：对真实报错调用 ai_ops.pipeline.diagnose()，
把入参与结构化结果原样落盘到 demo/samples/*.json，供演示页在完全离线时
通过同一个渲染器回看真实结论（不是手写、不是 mock）。

默认只从本地 var/data/ml/dataset.csv 按 id 重建标准化记录（不触生产库）；
已建规则的样例必须查库才有现场证据，此时跳过并明确提示（不造证据）；
未建规则长尾样例不触库，只要公网 LLM 可达即可生成。

如内网 Oracle 在线且已获读库授权，可显式加 --tlog 实时取数（ldate/lsection 最全）：
  uv run python demo/build_fixtures.py            # 默认：仅本地数据集 + 公网 LLM
  uv run python demo/build_fixtures.py --tlog     # 需显式授权：按 ID 查 ULOG.TLOG
"""
import csv
import json
import re
import socket
import sys
from datetime import datetime
from pathlib import Path

from ai_ops import paths
from ai_ops.config import load_config
from ai_ops.engine.rule_engine import Engine
from ai_ops.llm.client import LLMClient
from ai_ops.pipeline import diagnose

if "--tlog" in sys.argv:
    from ai_ops.engine.tlog import get_record_by_id

SAMPLES_DIR = Path(__file__).resolve().parent / "samples"

# (输出文件名, TLOG ID, 说明, force_llm)
JOBS = [
    ("position_4811525544.json", 4811525544,
     "旗舰案例：Au(T+N1) 买持仓不足（已建规则，强制 LLM 三证合一）", True),
    ("settle_4964465949.json", 4964465949,
     "期权结算价不存在（已建规则，自动走规则快速路径，零 token）", False),
    ("storage_493325942.json", 493325942,
     "长尾：交易员可用库存量不足（未建规则，LLM 兜底，无需查库）", True),
    ("login_636445574.json", 636445574,
     "长尾：用户名或密码错误（未建规则，自动升级 LLM，无需查库）", False),
    ("duration_1288703983.json", 1288703983,
     "长尾：存续期变更失败（未建规则，LLM 诚实低置信 + 排查方向）", True),
]

_DSN_HOSTPORT_RE = re.compile(r"@?([0-9A-Za-z_.\-]+):(\d+)")


def db_reachable(timeout=2.0):
    """对 config/db.yaml 的 DSN 做 TCP 预检，绝不触发 oracledb 长超时。"""
    cfg = load_config("db")
    dsn = cfg.get("dsn") or ""
    m = _DSN_HOSTPORT_RE.search(dsn)
    if not m:
        return False
    try:
        with socket.create_connection((m.group(1), int(m.group(2))), timeout=timeout):
            return True
    except OSError:
        return False


def rec_from_dataset(sid):
    """断库时从训练集按 id 重建标准化记录（字段与 pipeline 契约一致）。"""
    with open(paths.dataset_csv(), "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if str(row.get("id")) == str(sid):
                return {
                    "id": int(row["id"]),
                    "ldate": row.get("ldate", ""),
                    "llevel": int(row.get("llevel") or 0),
                    "errcode": int(row.get("errcode") or 0),
                    "func_no": row.get("func_no", ""),
                    "lsection": row.get("lsection", ""),
                    "text": (row.get("text") or "").strip(),
                }
    return None


def main():
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    use_tlog = "--tlog" in sys.argv
    online = use_tlog and db_reachable()
    if use_tlog:
        print("Oracle TCP 预检：%s" % ("可达，将按 ID 实时取数" if online else "不可达，改用 dataset.csv 重建记录"))
    else:
        print("默认模式：仅用本地 dataset.csv 重建记录（不触生产库；如需实时取数加 --tlog）")
    llm = LLMClient(load_config("llm"))
    # 离线样例是预跑制品、不在台上等，给足 90s 拿完整结论；
    # 演示页现场诊断仍用 12s 超时 + 诚实降级（见 demo/app.py）。
    llm.timeout = 90
    eng = Engine()   # 仅用于 match_type 判断是否需要查库（不触发连接）

    ok, skipped, failed = 0, 0, 0
    for fname, sid, desc, force_llm in JOBS:
        print("\n=== %s（ID=%s，%s）" % (fname, sid, desc))
        rec, rec_source = None, ""
        if online:
            try:
                rec = get_record_by_id(sid)
                rec_source = "tlog"
            except Exception as e:
                print("  TLOG 取数失败，回退 dataset.csv：%s" % e)
        if rec is None:
            rec = rec_from_dataset(sid)
            rec_source = "dataset"
        if rec is None:
            print("  跳过：dataset.csv 中也找不到 ID=%s" % sid)
            skipped += 1
            continue

        tcfg, _ = eng.match_type(rec["text"], rec.get("errcode") or 0)
        if tcfg is not None and not online:
            print("  跳过：该类型已建规则（%s），断库无法产出真实查库证据，不伪造" % tcfg.get("id"))
            skipped += 1
            continue

        try:
            res = diagnose(rec, force_llm=force_llm, llm=llm)
        except Exception as e:
            print("  失败：%s: %s" % (type(e).__name__, e))
            failed += 1
            continue

        payload = {
            "id": sid,
            "desc": desc,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "rec_source": rec_source,
            "force_llm": force_llm,
            "rec": rec,
            "res": res,
        }
        out = SAMPLES_DIR / fname
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
        print("  已写出 %s（来源=%s，结论来源=%s）" % (out, rec_source, res.get("source")))
        ok += 1

    print("\n完成：成功 %d，跳过 %d，失败 %d。样例目录：%s" % (ok, skipped, failed, SAMPLES_DIR))


if __name__ == "__main__":
    main()
