# -*- coding: utf-8 -*-
"""iQuant 固收量化系统实时监控对接（接口级，拉模式）。

与 Dimple 实时监控同构：通过 iQuant 平台暴露的 HTTP 接口，定时增量拉取
事中风控事件（日间异常风控事件），经字段映射后复用诊断内核自动诊断，
并 best-effort 落库，形成准实时闭环。

模块：
  - client.py   : IquantClient（明文鉴权、token 缓存/刷新、分页查询）
  - collector.py: 实时采集器（端点注册表、字段映射、增量幂等、调度入口）
"""

__all__ = ["client", "collector"]
