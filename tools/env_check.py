# -*- coding: utf-8 -*-
"""环境自检：Python 版本、第三方依赖、关键文件、本地模块、LLM 配置、数据库连通。
新机器/新环境跑一遍即可知道缺什么。用法：
    python tools/env_check.py
"""
import importlib
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)

print("=" * 80)
print("Python:", sys.version.split()[0], "| 解释器:", sys.executable)
print("项目目录:", _ROOT)

print("\n[1] 第三方依赖（requirements.txt）")
pkgs = [("yaml", "PyYAML"), ("oracledb", "oracledb"), ("sklearn", "scikit-learn"),
        ("joblib", "joblib"), ("numpy", "numpy"), ("scipy", "scipy")]
missing = []
for mod, dist in pkgs:
    try:
        m = importlib.import_module(mod)
        print("  [OK]   %-14s %s" % (dist, getattr(m, "__version__", "?")))
    except Exception as e:
        print("  [缺失] %-14s (%s)" % (dist, e.__class__.__name__))
        missing.append(dist)

print("\n[2] 关键文件 / 模型 / 数据")
for rel in ["diagnose.py", "hybrid_diagnose.py", "config/db.yaml", "config/llm.yaml",
            "models/routing.joblib", "models/biz_type.joblib",
            "data/ml/dataset.csv", "rules/errors.yaml"]:
    print("  %s  %s" % ("[OK]  " if os.path.exists(os.path.join(_ROOT, rel)) else "[缺失]", rel))

print("\n[3] 本地模块导入")
for mod in ["diagnose", "engine.parser", "engine.rule_engine", "ml.router",
            "ml.retriever", "llm.client"]:
    try:
        importlib.import_module(mod)
        print("  [OK]  ", mod)
    except Exception as e:
        print("  [失败]", mod, "->", repr(e))

print("\n[4] LLM 配置")
try:
    import yaml
    with open(os.path.join(_ROOT, "config/llm.yaml"), "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    print("  enabled=%s | model=%s | base=%s"
          % (cfg.get("enabled"), cfg.get("model"), cfg.get("base_url")))
except Exception as e:
    print("  [无法读取]", repr(e))

print("\n[5] 数据库连通（只读 SELECT 1 FROM DUAL）")
try:
    from engine.db import query
    cols, rows = query("SELECT 1 FROM DUAL")
    print("  [OK]  Oracle 连通，返回", rows)
except Exception as e:
    print("  [失败]", repr(e))

print("\n" + "=" * 80)
if missing:
    print("结论：缺少依赖 %s，请先执行：pip install -r requirements.txt" % missing)
else:
    print("结论：依赖与文件就绪；若数据库连通失败请检查 config/db.yaml 与网络。")
print("=" * 80)
