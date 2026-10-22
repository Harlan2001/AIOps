# -*- coding: utf-8 -*-
"""LLM 端点探测（OpenAI 兼容，标准库实现）：

    uv run python -m ai_ops.ops.llm_probe            # 最小对话连通自检
    uv run python -m ai_ops.ops.llm_probe --models   # 列出端点支持的模型（GET /models）

配置来自 config/llm.yaml（或 AIOPS_LLM_* 环境变量）；不打印 api_key。
"""
import argparse
import json
import urllib.error
import urllib.request

from ai_ops.config import load_config
from ai_ops.llm.client import LLMClient


def _http(method, url, key, body=None, timeout=40):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + key,
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except Exception as e:
        return -1, repr(e)


def list_models(cfg):
    base, key = cfg["base_url"].rstrip("/"), cfg.get("api_key", "EMPTY")
    print("GET", base + "/models")
    code, txt = _http("GET", base + "/models", key)
    print("status:", code)
    if code == 200:
        ids = [m.get("id") for m in json.loads(txt).get("data", [])]
        print("可用模型（%d 个）：" % len(ids))
        for i in ids:
            print("  -", i)
    else:
        print("返回：", txt[:1000])


def chat_ping():
    c = LLMClient()
    print("enabled =", c.enabled, "| model =", c.model, "| base =", c.base_url or "(未配置)")
    print("available =", c.available())
    reply = c.chat([{"role": "user", "content":
                     "你是连通性测试。只回复 JSON：{\"ok\":true}，不要输出其他内容。"}],
                   temperature=0.0)
    print("原始返回：", reply)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m ai_ops.ops.llm_probe")
    ap.add_argument("--models", action="store_true", help="列出端点支持的模型，不做对话")
    args = ap.parse_args(argv)

    cfg = load_config("llm")
    if not cfg or not cfg.get("base_url"):
        print("[未配置] config/llm.yaml 缺失或无 base_url；请参考 config/llm.yaml.example。")
        raise SystemExit(1)
    if args.models:
        list_models(cfg)
    else:
        chat_ping()


if __name__ == "__main__":
    main()
