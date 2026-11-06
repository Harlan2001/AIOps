# -*- coding: utf-8 -*-
"""全项目唯一的路径解析层。

优先级统一为：AIOPS_* 环境变量 > 仓库根下 var/（开发态，自动探测仓库根）
> 容器默认路径 /app。
- 开发态：本文件位于 <仓库根>/src/ai_ops/paths.py，向上查找同时含
  pyproject.toml 与 src/ai_ops 的目录即仓库根；
- 容器/已安装态：探测不到仓库根，路径全部来自环境变量或 /app 默认值，
  绝不靠 cwd 或 __file__ 上两级猜测。

var/ 整体 gitignore：模型、数据集、报告、KB 快照等运行时资产不入库，
镜像构建时 COPY 内部制品或运行时挂载。
"""
import os
from pathlib import Path

# 环境变量 -> (开发态相对仓库根路径, 容器默认路径)
_DIRS = {
    "config": ("config", "/app/config"),
    "reports": ("var/reports", "/app/reports"),
}


def _detect_repo_root():
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file() and (parent / "src" / "ai_ops").is_dir():
            return parent
    return None


REPO_ROOT = _detect_repo_root()


def _dir(kind, *, env, create=False):
    value = os.environ.get(env)
    if value:
        path = Path(value)
    elif REPO_ROOT:
        rel, _container = _DIRS[kind]
        path = REPO_ROOT / rel
    else:
        _rel, container = _DIRS[kind]
        path = Path(container)
    if create:
        path.mkdir(parents=True, exist_ok=True)
    return path


def config_dir():
    return _dir("config", env="AIOPS_CONFIG_DIR")


def config_file(name):
    """配置文件路径（name 不带扩展名），如 config_file('db') -> config/db.yaml。"""
    return config_dir() / (name + ".yaml")


def reports_dir():
    return _dir("reports", env="AIOPS_REPORTS_DIR", create=True)
