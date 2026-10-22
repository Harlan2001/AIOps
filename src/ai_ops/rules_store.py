# -*- coding: utf-8 -*-
"""规则包加载：包内基线 + 外挂发布目录（AIOPS_RULES_DIR）双层来源。

合并语义（必须保持确定性，支撑未来工作台"提交-审核-发布"）：
- runbook 正文 YAML：外挂同名文件整体覆盖包内基线；
- 类型注册表 errors.yaml：types 数组按 id 合并——外挂同 id 整条替换、
  新 id 追加到基线之后（只放外挂注册表不会丢基线类型）；
- noise_rules.yaml：noise_contains 数组去重追加；
- 外挂目录不存在时行为与纯包内基线完全一致。
"""
import os

import yaml
from importlib.resources import files

_PKG_FILES = files("ai_ops.assets.rules")


def external_dir():
    """外挂规则目录；未设置或目录不存在时返回 None。"""
    path = os.environ.get("AIOPS_RULES_DIR", "")
    return path if path and os.path.isdir(path) else None


def _pkg_yaml(rel):
    with _PKG_FILES.joinpath(*rel.split("/")).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _ext_yaml(rel):
    root = external_dir()
    if not root:
        return None
    path = os.path.join(root, *rel.split("/"))
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _merge_types(base, extra):
    """types 按 id 合并：同 id 替换（位置不变），新 id 追加。"""
    by_id = {t.get("id"): t for t in base}
    for t in extra:
        by_id[t.get("id")] = t
    return list(by_id.values())


def load_registries():
    """返回 (types, noise_contains)，已合并外挂覆盖层。"""
    errors = _pkg_yaml("errors.yaml") or {}
    noise = _pkg_yaml("noise_rules.yaml") or {}
    types = list(errors.get("types", []))
    noise_kw = list(noise.get("noise_contains", []))

    ext_errors = _ext_yaml("errors.yaml")
    if ext_errors:
        types = _merge_types(types, ext_errors.get("types", []))
    ext_noise = _ext_yaml("noise_rules.yaml")
    if ext_noise:
        for kw in ext_noise.get("noise_contains", []):
            if kw not in noise_kw:
                noise_kw.append(kw)
    return types, noise_kw


def load_runbook(name):
    """加载 runbook 正文；外挂 runbooks/<name>.yaml 优先。"""
    rel = "runbooks/%s.yaml" % name
    data = _ext_yaml(rel)
    if data is None:
        data = _pkg_yaml(rel)
    return data
