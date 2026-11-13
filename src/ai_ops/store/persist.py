# -*- coding: utf-8 -*-
"""best-effort 落库门面（方向一·阶段 0）。

- 持久化默认关闭（config/store.yaml enabled=false），关闭时完全不碰数据库；
- 开启后把诊断结果经仓储 upsert 落库；
- 任何落库异常都被吞掉并记录，绝不向上抛出，保证"记账"故障不阻断主诊断。
"""
import logging

from ..config import load_config
from . import diag_repo

_logger = logging.getLogger("ai_ops.store")


def is_enabled():
    """持久化总开关，缺省 false。"""
    return bool(load_config("store").get("enabled", False))


def persist_diagnosis(rec, out, trigger_type, batch_id=None,
                      diag_status="success", error_msg=None):
    """落库一条诊断；未启用直接返回 None，异常静默记录。"""
    if not is_enabled():
        return None
    try:
        entry = diag_repo.build_entry(
            rec, out, trigger_type, batch_id=batch_id,
            diag_status=diag_status, error_msg=error_msg)
        return diag_repo.upsert_log(entry)
    except Exception as e:  # noqa: BLE001 - 落库失败不得影响诊断主流程
        _logger.warning("诊断结果落库失败（已忽略）：%s: %s",
                        type(e).__name__, e)
        return None
