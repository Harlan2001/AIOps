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
    """持久化总开关，缺省 false；配置读取/解析异常时按关闭处理，不向主流程抛错。"""
    try:
        return bool(load_config("store").get("enabled", False))
    except Exception as e:  # noqa: BLE001 - 开关故障不得阻断诊断
        _logger.warning("读取持久化开关失败（按关闭处理）：%s: %s",
                        type(e).__name__, e)
        return False


def persist_diagnosis(rec, out, trigger_type, batch_id=None,
                      diag_status="success", error_msg=None):
    """落库一条诊断；未启用直接返回 None，异常静默记录。

    巡检（scheduled）用 upsert 去重；手工/批量事件用 insert 记为独立事件，
    不因内容指纹相同而互相覆盖。
    """
    if not is_enabled():
        return None
    try:
        entry = diag_repo.build_entry(
            rec, out, trigger_type, batch_id=batch_id,
            diag_status=diag_status, error_msg=error_msg)
        if trigger_type == "scheduled":
            return diag_repo.upsert_log(entry)
        return diag_repo.save_log(entry)
    except Exception as e:  # noqa: BLE001 - 落库失败不得影响诊断主流程
        _logger.warning("诊断结果落库失败（已忽略）：%s: %s",
                        type(e).__name__, e)
        return None
