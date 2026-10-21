# -*- coding: utf-8 -*-
"""验证 LLM 桥接链路：在本地起一个 OpenAI 兼容 mock 服务，
注入混合管线，确认"配好私有化 endpoint 即可调用"，并检查 JSON 解析与 LLM 报告渲染。
"""
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)

from llm.client import LLMClient          # noqa: E402
import hybrid_diagnose                    # noqa: E402


class MockHandler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        payload = self.rfile.read(n).decode("utf-8")
        try:
            req = json.loads(payload)
            content = req["messages"][-1]["content"]
        except Exception:
            content = ""
        # 模拟 LLM：根据证据返回结构化诊断（真实场景由私有化大模型完成）
        if "持仓不足" in content:
            answer = {"root": "（模拟LLM）买方向持仓不足：平仓量超过该客户可平量",
                      "actions": ["核对查库返回的 BUY_QTY 与本次平仓数量",
                                  "检查是否重复平仓或买卖方向选反",
                                  "调减平仓数量后重新提交"],
                      "confidence": 0.92, "need_more_evidence": False,
                      "evidence_note": "只读查库显示客户 0000000168 的 Au(T+N1) BUY_QTY=1999"}
        else:
            answer = {"root": "（模拟LLM）根据历史相似案例判断为该类数据缺失，需补齐基础数据",
                      "actions": ["核对对应基础数据表是否已生成", "重跑相关批处理任务"],
                      "confidence": 0.8, "need_more_evidence": True,
                      "evidence_note": "ML 召回存在高度相似历史案例"}
        body = json.dumps(
            {"choices": [{"message": {"role": "assistant",
                                      "content": json.dumps(answer, ensure_ascii=False)}}]},
            ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    srv = HTTPServer(("127.0.0.1", 8799), MockHandler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    llm = LLMClient()
    llm.enabled = True
    llm.base_url = "http://127.0.0.1:8799/v1"
    llm.api_key = "test"
    llm.model = "mock"
    assert llm.available()

    # 持仓不足，强制走 LLM（注入 mock）
    rec = {"id": 4811525544, "text": "平仓错误,[会员->016811][客户->0000000168][交易员->trader]"
           "[成交编号->20260827020000000317][合约->Au(T+N1)][买]持仓不足,尚缺<1>",
           "ldate": "2026-09-07 11:30:49", "errcode": 101028602,
           "lsection": "CLEAR.PKC_POSI.SP_CALC_OFFSET_DETAIL:3603", "func_no": None}
    res = hybrid_diagnose.diagnose(rec, force_llm=True, llm=llm)
    print(hybrid_diagnose.render(res))

    srv.shutdown()
    assert res["source"].startswith("LLM"), "LLM 路径未生效"
    assert res["answer"]["root"].startswith("（模拟LLM）"), "LLM 结论未被采用"
    print("LLM 桥接链路验证通过 ✔")


if __name__ == "__main__":
    main()
