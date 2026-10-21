# -*- coding: utf-8 -*-
"""探测 OpenAI 兼容端点支持的模型列表（GET /models），并可做一次最小对话自检。"""
import json
import os
import sys
import urllib.request
import urllib.error

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)

import yaml   # noqa: E402


def load_cfg():
    with open(os.path.join(_ROOT, "config", "llm.yaml"), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def http(method, url, key, body=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + key,
    })
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except Exception as e:
        return -1, repr(e)


def main():
    cfg = load_cfg()
    base, key = cfg["base_url"].rstrip("/"), cfg["api_key"]
    print("GET", base + "/models")
    code, txt = http("GET", base + "/models", key)
    print("status:", code)
    if code == 200:
        data = json.loads(txt)
        ids = [m.get("id") for m in data.get("data", [])]
        print("可用模型（%d 个）：" % len(ids))
        for i in ids:
            print("  -", i)
    else:
        print("返回：", txt[:1000])


if __name__ == "__main__":
    main()
