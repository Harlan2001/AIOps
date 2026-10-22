# -*- coding: utf-8 -*-
"""全项目唯一的路径解析层。

优先级统一为：AIOPS_* 环境变量 > 仓库根（开发态，自动探测）> 容器默认路径 /app。
- 开发态：本文件位于 <仓库根>/src/ai_ops/paths.py，向上查找同时含
  pyproject.toml 与 src/ai_ops 的目录即仓库根；
- 容器/已安装态：探测不到仓库根，路径全部来自环境变量或 /app 默认值，
  绝不靠 cwd 或 __file__ 上两级猜测。
"""
import os
from pathlib import Path


def _detect_repo_root():
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file() and (parent / "src" / "ai_ops").is_dir():
            return parent
    return None


REPO_ROOT = _detect_repo_root()


def _env_dir(name):
    value = os.environ.get(name)
    return Path(value) if value else None


def _default(*, rel, container):
    env = _env_dir("AIOPS_" + rel.upper() + "_DIR")
    if env:
        return env
    if REPO_ROOT:
        return REPO_ROOT / rel
    return Path(container)


def config_dir():
    return _default(rel="config", container="/app/config")


def config_file(name):
    """配置文件路径（name 不带扩展名），如 config_file('db') -> config/db.yaml。"""
    return config_dir() / (name + ".yaml")


def models_dir():
    return _default(rel="models", container="/app/models")


def data_dir():
    return _default(rel="data", container="/app/data")


def dataset_csv():
    """ML 训练数据集（带标签的全量历史日志）。"""
    return data_dir() / "ml" / "dataset.csv"


def reports_dir():
    path = _default(rel="reports", container="/app/reports")
    path.mkdir(parents=True, exist_ok=True)
    return path
