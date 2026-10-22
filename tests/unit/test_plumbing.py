# -*- coding: utf-8 -*-
"""路径解析、配置环境覆盖、证据格式化、空召回降级、CLI 出口码、报告渲染冒烟。"""
import pytest

from ai_ops import evidence, paths, reporting


# ---------- paths ----------

def test_paths_layout():
    assert paths.REPO_ROOT is not None
    assert str(paths.dataset_csv()).replace("\\", "/").endswith("var/data/ml/dataset.csv")
    assert str(paths.config_file("db")).replace("\\", "/").endswith("config/db.yaml")


def test_paths_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv("AIOPS_MODELS_DIR", str(tmp_path / "m"))
    assert str(paths.models_dir()) == str(tmp_path / "m")


# ---------- config ----------

def test_config_kb_env_override(monkeypatch):
    # 仓库不跟踪 config/kb.yaml：文件缺失 + 环境变量注入
    monkeypatch.delenv("AIOPS_KB_ENABLED", raising=False)
    from ai_ops.config import load_config
    monkeypatch.setenv("AIOPS_KB_ENABLED", "false")
    monkeypatch.setenv("AIOPS_KB_TOP", "5")
    cfg = load_config("kb")
    assert cfg["enabled"] is False
    assert cfg["top"] == 5


# ---------- evidence ----------

def test_evidence_clip_join():
    assert evidence.clip(None) == ""
    assert evidence.clip("a\nb") == "a b"
    assert len(evidence.clip("x" * 300, 10)) == 11  # 截断加省略号
    assert evidence.join(["a", "", "b"]) == "a；b"
    assert evidence.join("直接字符串") == "直接字符串"


_CARD = {"knowledge_version": "v9", "baseline_id": "b1", "matched_document_count": 1,
         "runtime_verified": False, "cards": [{
             "title": "持仓不足", "document_id": "D12", "score": 8.5,
             "symptom": "平仓时报持仓不足", "required_facts": ["客户可平量"],
             "parameter_codes": ["BUY_QTY"],
             "branches": [{"id": "B1", "when_all": ["方向选反"], "exclude_when": [],
                           "next_checks": ["查 BUY_QTY"], "actions": [{
                               "title": "调减平仓量", "allowed_when": ["确认"],
                               "forbidden_when": [], "side_effects": [],
                               "verification": ["重提"], "rollback_boundary": ""}]}],
             "readonly_queries": [], "log_context": [], "n_queries": 0, "n_logs": 0,
             "sources": [{"repository": "core", "path": "x.sql", "symbol": "f"}]}]}


def test_evidence_card_formatters():
    block = evidence.to_prompt_block(_CARD)
    assert "知识卡 1" in block and "方向选反" in block and "冻结源码取证" in block
    lines = evidence.to_report_lines(_CARD)
    assert any("持仓不足" in x for x in lines)
    assert "未命中" in evidence.to_prompt_block(None)
    assert evidence.to_report_lines({})[0].endswith("知识库未命中相关诊断材料）")


# ---------- retriever 空降级 ----------

def test_retriever_degrades_without_dataset(tmp_path):
    from ai_ops.ml.retriever import SimilarCaseIndex
    idx = SimilarCaseIndex.from_dataset(path=str(tmp_path / "missing.csv"))
    assert idx.records == [] and idx.query("任意文本") == []


# ---------- CLI 出口码 ----------

def test_cli_no_args_exit_2(monkeypatch):
    from ai_ops import cli
    with pytest.raises(SystemExit) as ei:
        cli.main([])
    assert ei.value.code == 2


# ---------- 报告渲染冒烟 ----------

def test_render_rule_noise():
    out = reporting.render_rule(
        {"class": "noise", "text": "处理成功！", "verdict": "非故障提示，无需诊断"})
    assert "TLOG 业务报错诊断报告" in out and "非故障提示" in out


def test_render_hybrid_minimal():
    res = {"text": "x", "errcode": 0, "ldate": "", "loc": "",
           "rt": {"route": "noise", "confidence": 1.0},
           "cases": [], "rule_res": None, "kb_card": None,
           "answer": {"root": "无需诊断", "actions": [], "confidence": 1.0},
           "source": "ML 快速路径"}
    out = reporting.render_hybrid(res)
    assert "ML 分流" in out and "ML 快速路径" in out
