# -*- coding: utf-8 -*-
"""巡检执行器（方向一·阶段 1）。

流程：生成批次号 → 遍历来源/业务日期 → 只读取数 → 逐项隔离诊断 → best-effort 落库。
特性：
  - 进程内并发锁：上一轮未跑完时直接跳过本轮，防止任务重叠；
  - 逐来源 try/except：单个来源失败不影响其他来源；
  - 完全复用 DiagnosticService，落库与否由 store 开关决定（本模块不直接写库）。
"""
import logging
import threading
import uuid
from datetime import datetime, timedelta

from ..config import load_config
from ..service import MAX_BATCH, DiagnosticService

_logger = logging.getLogger("ai_ops.scheduler")

# 进程内并发锁，防止巡检重叠。
_RUN_LOCK = threading.Lock()

_DEFAULTS = {
    "interval_minutes": 120,
    "lookback_days": 1,
    "batch_size": MAX_BATCH,
}


def load_schedule():
    """读取巡检配置并补默认值。"""
    cfg = load_config("schedule")
    out = dict(_DEFAULTS)
    out.update(cfg)
    return out


def _target_dates(lookback_days):
    """最近 N 个自然日的 yyyyMMdd 列表（含当天，按日期升序）。"""
    n = max(1, int(lookback_days or 1))
    today = datetime.now()
    return [
        (today - timedelta(days=i)).strftime("%Y%m%d")
        for i in range(n - 1, -1, -1)
    ]


def is_scheduled():
    """巡检是否启用。"""
    return bool(load_schedule().get("enabled", False))


def run_inspection(svc=None):
    """执行一次巡检，返回本次巡检摘要；未获锁或未启用时返回相应状态。"""
    cfg = load_schedule()
    if not cfg.get("enabled", False):
        return {"status": "disabled"}

    # 非阻塞抢锁：上一轮仍在运行则跳过本轮。
    if not _RUN_LOCK.acquire(blocking=False):
        _logger.warning("上一轮巡检尚未结束，跳过本次触发")
        return {"status": "skipped"}

    service = svc or DiagnosticService()
    batch_id = uuid.uuid4().hex
    sources_cfg = cfg.get("sources") or []
    source_ids = list(sources_cfg) if sources_cfg else list(service.sources())
    dates = _target_dates(cfg.get("lookback_days"))
    batch_size = max(1, min(int(cfg.get("batch_size") or MAX_BATCH), MAX_BATCH))

    summary = {
        "status": "ok", "batch_id": batch_id,
        "sources": source_ids, "dates": dates,
        "scanned": 0, "diagnosed": 0, "errors": 0, "by_source": {},
    }
    try:
        for sid in source_ids:
            src_scanned = 0
            src_errors = 0
            for date in dates:
                try:
                    recs = service.list_records(sid, date, limit=batch_size)
                    pairs = service.diagnose_many_isolated(
                        recs,
                        _ctx={"trigger_type": "scheduled", "batch_id": batch_id})
                except Exception as e:  # noqa: BLE001 - 单来源/日期失败隔离
                    _logger.warning("巡检 %s %s 失败（已跳过）：%s",
                                    sid, date, e)
                    src_errors += 1
                    continue
                src_scanned += len(pairs)
                src_errors += sum(
                    1 for _r, res in pairs
                    if isinstance(res, dict) and res.get("_diagnose_error"))
            summary["scanned"] += src_scanned
            summary["errors"] += src_errors
            summary["by_source"][sid] = {
                "scanned": src_scanned, "errors": src_errors}
        summary["diagnosed"] = summary["scanned"] - summary["errors"]
    finally:
        _RUN_LOCK.release()

    _logger.info("巡检完成 batch=%s 扫描=%d 异常=%d",
                 batch_id, summary["scanned"], summary["errors"])
    return summary
