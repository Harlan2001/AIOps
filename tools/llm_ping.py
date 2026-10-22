# -*- coding: utf-8 -*-
"""最小连通测试：验证 config/llm.yaml 配置的模型可正常对话。"""
from ai_ops.llm.client import LLMClient

c = LLMClient()
print("enabled =", c.enabled, "| model =", c.model, "| base =", c.base_url)
print("available =", c.available())
reply = c.chat([{"role": "user", "content": "你是连通性测试。只回复 JSON：{\"ok\":true}，不要输出其他内容。"}],
               temperature=0.0)
print("原始返回：", reply)
