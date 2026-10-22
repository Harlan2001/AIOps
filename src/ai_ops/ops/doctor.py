# -*- coding: utf-8 -*-
"""环境自检：Python/依赖、关键资产路径、包模块导入、LLM 配置、Oracle 连通。
新机器或新容器跑一遍即可知道缺什么：

    uv run python -m ai_ops.ops.doctor
"""
import importlib
import sys

from ai_ops import paths, rules_store

_PKGS = [("yaml", "PyYAML"), ("oracledb", "oracledb"), ("sklearn", "scikit-learn"),
         ("joblib", "joblib"), ("numpy", "numpy"), ("scipy", "scipy")]

_MODULES = ["ai_ops.cli", "ai_ops.pipeline", "ai_ops.reporting",
            "ai_ops.engine.parser", "ai_ops.engine.rule_engine",
            "ai_ops.ml.router", "ai_ops.ml.retriever",
            "ai_ops.llm.client", "ai_ops.kb.client"]


def main():
    missing = []
    print("=" * 80)
    print("Python:", sys.version.split()[0], "| 解释器:", sys.executable)
    print("仓库根  :", paths.REPO_ROOT or "(已安装态，路径来自环境变量或 /app)")

    print("\n[1] 第三方依赖（uv sync 安装，见 pyproject.toml）")
    for mod, dist in _PKGS:
        try:
            m = importlib.import_module(mod)
            print("  [OK]   %-14s %s" % (dist, getattr(m, "__version__", "?")))
        except Exception as e:
            print("  [缺失] %-14s (%s)" % (dist, e.__class__.__name__))
            missing.append(dist)

    print("\n[2] 配置 / 模型 / 数据 / 规则资产")
    cfg_dir = paths.config_dir()
    assets = [
        ("config/db.yaml.example 模板", cfg_dir / "db.yaml.example"),
        ("config/db.yaml（真实值，不入库）", paths.config_file("db")),
        ("config/llm.yaml（未配置则离线降级）", paths.config_file("llm")),
        ("routing.joblib", paths.models_dir() / "routing.joblib"),
        ("biz_type.joblib", paths.models_dir() / "biz_type.joblib"),
        ("ML 数据集 dataset.csv", paths.dataset_csv()),
    ]
    for label, path in assets:
        print("  %s  %s (%s)" % ("[OK]  " if path.exists() else "[缺失]", label, path))
    try:
        types, noise = rules_store.load_registries()
        print("  [OK]   规则资产已装载（类型 %d、噪音关键词 %d；外部覆盖目录：%s）"
              % (len(types), len(noise), rules_store.external_dir() or "无"))
    except Exception as e:
        print("  [失败] 规则资产装载：%r" % e)
        missing.append("rules")

    print("\n[3] 包模块导入")
    for mod in _MODULES:
        try:
            importlib.import_module(mod)
            print("  [OK]  ", mod)
        except Exception as e:
            print("  [失败]", mod, "->", repr(e))
            missing.append(mod)

    print("\n[4] LLM 配置（不打印 api_key）")
    from ai_ops.config import load_config
    cfg = load_config("llm")
    if cfg:
        print("  enabled=%s | model=%s | base=%s | timeout=%s"
              % (cfg.get("enabled"), cfg.get("model"), cfg.get("base_url"),
                 cfg.get("timeout", 30)))
    else:
        print("  [未配置] config/llm.yaml 缺失：诊断将走规则/兜底快速路径（离线可跑）")

    print("\n[5] 数据库连通（只读 SELECT 1 FROM DUAL）")
    try:
        from ai_ops.engine.db import query
        _cols, rows = query("SELECT 1 FROM DUAL")
        print("  [OK]  Oracle 连通，返回", rows)
    except Exception as e:
        print("  [失败]", repr(e))

    print("\n" + "=" * 80)
    if missing:
        print("结论：存在未就绪项 %s；请先 uv sync，并按 config/*.example 放置配置/资产。"
              % missing)
        sys.exit(1)
    print("结论：依赖与资产就绪；数据库连通失败请检查 config/db.yaml 与内网/VPN。")
    print("=" * 80)


if __name__ == "__main__":
    main()
