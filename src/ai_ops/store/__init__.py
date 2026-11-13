# -*- coding: utf-8 -*-
"""诊断结果持久化存储包（方向一·阶段 0）。

- connection：独立、受管控的写连接（与引擎只读 query 隔离）；
- diag_repo：诊断日志的领域仓储（指纹去重、落库、后续查询/标注）；
- persist：best-effort 落库门面，供 service 调用，失败不阻断诊断。
"""
