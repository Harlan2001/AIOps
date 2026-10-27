# -*- coding: utf-8 -*-
"""三份 YAML 配置的统一加载入口。

约定：
- 仓库只跟踪 config/*.example，真实 yaml 不入库，由挂载或环境变量注入；
- 字段级环境变量覆盖（AIOPS_<域>_<字段>），供 Docker Compose 注入密钥；
- llm / kb 配置缺失时返回 {}（静默降级语义由调用方保持）；
- db 配置只在真正连库时才要求存在，缺失给出明确的复制指引。
"""
import os

import yaml

from . import paths

_ENV_PREFIX = {
    "db": "AIOPS_DB_",
    "llm": "AIOPS_LLM_",
    "kb": "AIOPS_KB_",
}

# 允许被环境变量覆盖的字段（值为环境变量后缀，统一大写下划线）
_OVERRIDES = {
    "db": {"user": "USER", "password": "PASSWORD", "host": "HOST",
           "port": "PORT", "database": "DATABASE"},
    "llm": {"enabled": "ENABLED", "base_url": "BASE_URL", "api_key": "API_KEY",
            "model": "MODEL", "timeout": "TIMEOUT"},
    "kb": {"enabled": "ENABLED", "kb_root": "ROOT", "audience": "AUDIENCE",
           "baseline": "BASELINE", "top": "TOP", "execute_kb_sql": "EXECUTE_SQL"},
}

_BOOL = {"enabled", "execute_kb_sql"}
_INT = {"timeout", "top", "port"}


def _coerce(key, value):
    if key in _BOOL:
        return str(value).strip().lower() in ("1", "true", "yes", "on")
    if key in _INT:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
    return value


def _load_yaml(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        return {}


def load_config(name, *, required=False):
    """加载 config/<name>.yaml 并叠加环境变量覆盖。"""
    cfg = _load_yaml(paths.config_file(name))
    prefix = _ENV_PREFIX[name]
    for key, suffix in _OVERRIDES[name].items():
        env_key = prefix + suffix
        if os.environ.get(env_key):
            value = _coerce(key, os.environ[env_key])
            if value is not None:
                cfg[key] = value
    if required and not cfg:
        example = paths.config_file(name + ".example")
        raise FileNotFoundError(
            "缺少配置 %s；请复制模板：%s -> %s（或用 %s* 环境变量注入）"
            % (paths.config_file(name), example.name,
               paths.config_file(name).name, prefix))
    return cfg
