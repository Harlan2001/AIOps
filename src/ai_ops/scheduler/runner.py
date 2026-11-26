# -*- coding: utf-8 -*-
"""APScheduler 进程内调度封装（方向一·阶段 1 + Dimple 实时监控）。

同一个 AsyncIOScheduler 管理三类相互独立的 job，各自有配置开关：
  - aiops_inspection：GaussDB 错误表巡检（schedule.enabled，cron 或固定间隔）；
  - dimple_realtime  ：Dimple 接口实时采集（dimple.enabled，固定间隔，准实时）；
  - iquant_realtime  ：iQuant 事中风控事件实时采集（iquant.enabled，固定间隔，准实时）。
三者均 max_instances=1 + coalesce，杜绝进程内任务重叠与补偿堆积；
iQuant 采集另持游标跨进程文件锁，多 API worker 不会重复拉取与并发写游标。
所有任务都未启用时返回 None，服务行为与现状完全一致。
"""
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from ..dimple import collector as dimple_collector
from ..iquant import collector as iquant_collector
from . import inspector

_logger = logging.getLogger("ai_ops.scheduler")


def _add_inspection_job(scheduler, svc):
    cfg = inspector.load_schedule()
    job_kwargs = {
        "func": inspector.run_inspection,
        "kwargs": {"svc": svc},
        "max_instances": 1,
        "coalesce": True,
        "id": "aiops_inspection",
        "replace_existing": True,
    }
    cron = (cfg.get("cron") or "").strip()
    if cron:
        scheduler.add_job(trigger=CronTrigger.from_crontab(cron), **job_kwargs)
    else:
        scheduler.add_job(
            trigger="interval",
            minutes=int(cfg.get("interval_minutes") or 120),
            **job_kwargs)


def _add_dimple_job(scheduler, svc):
    cfg = dimple_collector.load_dimple_config()
    scheduler.add_job(
        func=dimple_collector.run_realtime_collection,
        kwargs={"svc": svc},
        trigger="interval",
        minutes=int(cfg.get("interval_minutes") or 5),
        max_instances=1,
        coalesce=True,
        id="dimple_realtime",
        replace_existing=True)


def _add_iquant_job(scheduler, svc):
    cfg = iquant_collector.load_iquant_config()
    scheduler.add_job(
        func=iquant_collector.run_realtime_collection,
        kwargs={"svc": svc},
        trigger="interval",
        minutes=int(cfg.get("interval_minutes") or 5),
        max_instances=1,
        coalesce=True,
        id="iquant_realtime",
        replace_existing=True)


def build_scheduler(svc=None):
    """按配置创建（未启动的）调度器；所有任务都未启用时返回 None。"""
    inspection_on = bool(inspector.load_schedule().get("enabled", False))
    dimple_on = bool(dimple_collector.load_dimple_config().get("enabled", False))
    iquant_on = bool(iquant_collector.load_iquant_config().get("enabled", False))
    if not inspection_on and not dimple_on and not iquant_on:
        return None

    scheduler = AsyncIOScheduler()
    if inspection_on:
        _add_inspection_job(scheduler, svc)
    if dimple_on:
        _add_dimple_job(scheduler, svc)
    if iquant_on:
        _add_iquant_job(scheduler, svc)
    return scheduler


def start_scheduler(scheduler):
    """启动调度器（需在事件循环内调用）。"""
    if scheduler is None:
        return
    scheduler.start()
    for job in scheduler.get_jobs():
        _logger.info("定时任务已启动：%s（下次触发 %s）", job.id, job.next_run_time)


def shutdown_scheduler(scheduler):
    """关闭调度器；不等待正在执行的任务。"""
    if scheduler is not None and scheduler.running:
        scheduler.shutdown(wait=False)
