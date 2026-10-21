# -*- coding: utf-8 -*-
"""最小连通测试：验证 config/llm.yaml 配置的模型可正常对话。"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)

from llm.client import LLMClient   # noqa: E402

c = LLMClient()
print("enabled =", c.enabled, "| model =", c.model, "| base =", c.base_url)
print("available =", c.available())
reply = c.chat([{"role": "user", "content": "你是连通性测试。只回复 JSON：{\"ok\":true}，不要输出其他内容。"}],
               temperature=0.0)
print("原始返回：", reply)
