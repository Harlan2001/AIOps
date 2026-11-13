# -*- coding: utf-8 -*-
"""APScheduler 进程内调度封装（方向一·阶段 1·方案 A）。

- 仅在 schedule.enabled=true 时创建并启动；
- 支持 cron 表达式或固定间隔（interval_minutes）；
- max_instances=1 + coalesce 配合 inspector 的进程锁，杜绝任务重叠与补偿堆积。
"""
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from . import inspector

_logger = logging.getLogger("ai_ops.scheduler")


def build_scheduler(svc=None):
    """按配置创建（未启动的）调度器；未启用返回 None。"""
    cfg = inspector.load_schedule()
    if not cfg.get("enabled", False):
        return None

    scheduler = AsyncIOScheduler()
    cron = (cfg.get("cron") or "").strip()
    job_kwargs = {
        "func": inspector.run_inspection,
        "kwargs": {"svc": svc},
        "max_instances": 1,
        "coalesce": True,
        "id": "aiops_inspection",
        "replace_existing": True,
    }
    if cron:
        scheduler.add_job(trigger=CronTrigger.from_crontab(cron), **job_kwargs)
    else:
        scheduler.add_job(
            trigger="interval",
            minutes=int(cfg.get("interval_minutes") or 120),
            **job_kwargs)
    return scheduler


def start_scheduler(scheduler):
    """启动调度器（需在事件循环内调用）。"""
    if scheduler is None:
        return
    scheduler.start()
    _logger.info("定时巡检已启动：%s", scheduler.get_job("aiops_inspection"))


def shutdown_scheduler(scheduler):
    """关闭调度器；不等待正在执行的任务。"""
    if scheduler is not None and scheduler.running:
        scheduler.shutdown(wait=False)
