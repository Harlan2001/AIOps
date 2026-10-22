# -*- coding: utf-8 -*-
"""集成测试：本地起 OpenAI 兼容 mock 服务，注入 LLMClient 走完整混合管线，
验证"配好私有化 endpoint 即可调用"——JSON 解析、结论采用、报告渲染全链路。

离线安全：选用未建规则的业务报错，规则引擎在类型匹配阶段即返回，不连 Oracle。
（需要查库取证的端到端链路在内网环境用 scripts/llm_demo_batch.py 验证。）
"""
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from ai_ops import pipeline, reporting
from ai_ops.llm.client import LLMClient

ANSWER = {"root": "（模拟LLM）登录用户名或密码错误，多为账号锁定/密码过期",
          "actions": ["引导用户重置密码", "检查账户锁定状态"],
          "confidence": 0.83}


class MockHandler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        self.rfile.read(n)
        body = json.dumps(
            {"choices": [{"message": {"role": "assistant",
                                      "content": json.dumps(ANSWER, ensure_ascii=False)}}]},
            ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


@pytest.fixture(scope="module")
def mock_llm():
    srv = HTTPServer(("127.0.0.1", 8799), MockHandler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    llm = LLMClient()
    llm.enabled = True
    llm.base_url = "http://127.0.0.1:8799/v1"
    llm.api_key = "test"
    llm.model = "mock"
    assert llm.available()
    yield llm
    srv.shutdown()


def test_llm_bridge(mock_llm):
    rec = {"text": "登录的时候提示用户名密码不对", "ldate": "2026-09-07 11:30:49",
           "errcode": 0, "lsection": "", "func_no": None}
    res = pipeline.diagnose(rec, force_llm=True, llm=mock_llm)
    assert res["source"].startswith("LLM"), res["source"]
    assert res["answer"]["root"] == ANSWER["root"]
    report = reporting.render_hybrid(res)
    assert "【最终诊断】来源：LLM" in report
    assert ANSWER["root"] in report
