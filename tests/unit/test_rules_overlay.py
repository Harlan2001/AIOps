# -*- coding: utf-8 -*-
"""规则包双层来源与合并语义：包内基线 + AIOPS_RULES_DIR 外挂覆盖。"""
import pytest

from ai_ops import rules_store


def test_baseline_registries():
    types, noise = rules_store.load_registries()
    assert [t["id"] for t in types] == [
        "settle_price_not_found", "defer_fee_not_found", "position_not_enough"]
    assert noise and all(isinstance(k, str) for k in noise)
    rb = rules_store.load_runbook("rb_position")
    assert isinstance(rb, dict) and rb.get("steps")


def test_external_dir_default_empty(monkeypatch):
    monkeypatch.delenv("AIOPS_RULES_DIR", raising=False)
    assert rules_store.external_dir() is None


def test_overlay_types_same_id_replace_keeps_position_new_appends(tmp_path, monkeypatch):
    (tmp_path / "runbooks").mkdir()
    (tmp_path / "errors.yaml").write_text(
        "types:\n"
        "  - id: settle_price_not_found\n"
        "    title: 被外挂替换的标题\n"
        "    keywords: [\"结算价不存在\"]\n"
        "    runbook: rb_settle_price\n"
        "  - id: brand_new_type\n"
        "    title: 外挂新增类型\n"
        "    keywords: [\"不存在的新症状\"]\n"
        "    runbook: rb_settle_price\n",
        encoding="utf-8")
    monkeypatch.setenv("AIOPS_RULES_DIR", str(tmp_path))

    types, _ = rules_store.load_registries()
    by_id = {t["id"]: t for t in types}
    # 同 id 替换且位置不变；基线另外两型不丢；新 id 追加在最后
    assert [t["id"] for t in types] == [
        "settle_price_not_found", "defer_fee_not_found",
        "position_not_enough", "brand_new_type"]
    assert by_id["settle_price_not_found"]["title"] == "被外挂替换的标题"


def test_overlay_noise_dedup_append(tmp_path, monkeypatch):
    base_types, base_noise = rules_store.load_registries()
    (tmp_path / "noise_rules.yaml").write_text(
        "noise_contains:\n  - %r\n  - \"__全新噪音关键词__\"\n" % base_noise[0],
        encoding="utf-8")
    monkeypatch.setenv("AIOPS_RULES_DIR", str(tmp_path))

    _, noise = rules_store.load_registries()
    assert "__全新噪音关键词__" in noise
    assert len(noise) == len(base_noise) + 1  # 基线词去重不重复追加


def test_overlay_runbook_file_overrides_package(tmp_path, monkeypatch):
    rb_dir = tmp_path / "runbooks"
    rb_dir.mkdir()
    (rb_dir / "rb_settle_price.yaml").write_text(
        "id: rb_settle_price\noverlay_marker: true\nsteps: []\n", encoding="utf-8")
    monkeypatch.setenv("AIOPS_RULES_DIR", str(tmp_path))

    rb = rules_store.load_runbook("rb_settle_price")
    assert rb.get("overlay_marker") is True and rb["steps"] == []


def test_overlay_dir_missing_equals_baseline(tmp_path, monkeypatch):
    monkeypatch.delenv("AIOPS_RULES_DIR", raising=False)
    base_types, base_noise = rules_store.load_registries()
    monkeypatch.setenv("AIOPS_RULES_DIR", str(tmp_path / "not-exist"))
    types, noise = rules_store.load_registries()
    assert [t["id"] for t in types] == [t["id"] for t in base_types]
    assert noise == base_noise
