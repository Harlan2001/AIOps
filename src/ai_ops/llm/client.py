# -*- coding: utf-8 -*-
"""LLM 客户端：OpenAI 兼容接口（标准库 urllib 实现，无需额外依赖）。

- config/llm.yaml enabled=true 且 base_url 可用时，调用私有化大模型；
- 未配置或调用失败时，available() 为 False / diagnose() 返回 None，
  编排层自动回退到规则引擎（保证离线、无 LLM 也能跑）。
"""
import json
import urllib.request
import urllib.error

from ai_ops.config import load_config
from ai_ops.llm import prompts


class LLMClient:
    def __init__(self, cfg=None):
        # 未配置 / 缺文件时 cfg 为 {}：available()=False，编排层静默回退规则
        cfg = cfg if cfg is not None else load_config("llm")
        self.enabled = bool(cfg.get("enabled"))
        self.base_url = (cfg.get("base_url") or "").rstrip("/")
        self.api_key = cfg.get("api_key", "EMPTY")
        self.model = cfg.get("model", "")
        self.timeout = int(cfg.get("timeout", 30))

    def available(self):
        return bool(self.enabled and self.base_url)

    def chat(self, messages, temperature=0.1):
        if not self.available():
            return None
        url = self.base_url + "/chat/completions"
        body = json.dumps({
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 1500,
        }).encode("utf-8")
        req = urllib.request.Request(
            url, data=body,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer " + self.api_key})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            print("[LLM] HTTP %s 错误：%s" % (e.code, detail[:600]))
            return None
        except Exception as e:
            print("[LLM] 调用失败，将回退规则引擎：%s" % e)
            return None

    def diagnose(self, ctx):
        """返回结构化诊断 dict；不可用/失败返回 None。"""
        raw = self.chat(prompts.build_messages(ctx))
        if raw is None:
            return None
        parsed = prompts.safe_parse_json(raw)
        if parsed is None:
            return {"root": raw, "actions": [], "confidence": 0.0,
                    "need_more_evidence": True, "evidence_note": "LLM 未按 JSON 返回",
                    "_raw": True}
        return parsed
