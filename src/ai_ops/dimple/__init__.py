# -*- coding: utf-8 -*-
"""Dimple 实时监控对接（接口级，拉模式）。

通过 Dimple 平台暴露的 HTTP 接口，定时增量拉取实时监控数据（合规预警等），
经字段映射后复用诊断内核自动诊断，并 best-effort 落库，形成准实时闭环。

模块：
  - crypto.py   : RSA 公钥加密（登录密码，纯标准库 PKCS#1 v1.5）
  - client.py   : DimpleClient（鉴权、token 缓存/刷新、分页查询）
  - collector.py: 实时采集器（端点注册表、字段映射、增量幂等、调度入口）
"""

__all__ = ["crypto", "client", "collector"]
