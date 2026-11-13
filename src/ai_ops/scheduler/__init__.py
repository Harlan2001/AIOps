# -*- coding: utf-8 -*-
"""定时巡检包（方向一·阶段 1，方案 A：进程内 APScheduler）。

- inspector：巡检执行逻辑，复用取数与诊断，含并发锁与逐来源异常隔离；
- runner：AsyncIOScheduler 的创建/启停，按配置调度 inspector。
"""
