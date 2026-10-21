# -*- coding: utf-8 -*-
"""批量探测候选模型，找出当前 API-Key 实际有权限调用（chat/completions 返回 200）的模型。"""
import json
import os
import sys
import urllib.request
import urllib.error

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)

import yaml   # noqa: E402

CANDIDATES = [
    "cmaas-qwen3.8-flash", "qwen3.8-flash", "qwen3.8-max", "qwen3.8-max-0902",
    "qwen-plus", "qwen-plus-latest", "qwen-turbo-2024-11-01", "qwen-max", "qwen-flash",
    "deepseek-v4.1-flash", "deepseek-v4-pro", "vanchin/deepseek-v3",
    "glm-5.3-prime", "glm-5.3", "kimi/kimi-k3", "MiniMax/MiniMax-M3",
    "sre-gpu-auto-handle", "test-sre-gpu-auto-handle",
    "qwen3-coder-flash", "qwen2.5-1.5b-instruct",
]


def main():
    with open(os.path.join(_ROOT, "config", "llm.yaml"), "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    base, key = cfg["base_url"].rstrip("/"), cfg["api_key"]
    ok = []
    for m in CANDIDATES:
        body = json.dumps({
            "model": m,
            "messages": [{"role": "user", "content": "hi"}],
            "max_tokens": 4,
        }).encode("utf-8")
        req = urllib.request.Request(base + "/chat/completions", data=body, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + key,
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"].get("content", "")
            print("  [OK]   %-28s -> %s" % (m, content[:20].replace("\n", " ")))
            ok.append(m)
        except urllib.error.HTTPError as e:
            try:
                code = json.loads(e.read().decode("utf-8")).get("error", {}).get("code", e.code)
            except Exception:
                code = e.code
            print("  [%s] %s" % (str(code).upper()[:4] if code else e.code, m))
        except Exception as e:
            print("  [ERR]  %-28s %s" % (m, repr(e)[:60]))
    print("=" * 70)
    print("当前 Key 可调用的模型：", ok)


if __name__ == "__main__":
    main()
