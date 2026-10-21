# -*- coding: utf-8 -*-
"""ML 分流器加载与推理（毫秒级、本地、可离线）。

输出两级判断 + 置信度：
  route      : noise / biz / ora / other
  biz_type   : 业务报错的 Top30 类型骨架或 other_biz
置信度低于阈值的，编排层升级给 LLM（方案三的"高置信走快速路径"）。
"""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)

import joblib   # noqa: E402


class Router:
    def __init__(self, model_dir=None):
        model_dir = model_dir or os.path.join(_ROOT, "models")
        self.cls_route = joblib.load(os.path.join(model_dir, "routing.joblib"))
        self.cls_biz = joblib.load(os.path.join(model_dir, "biz_type.joblib"))
        with open(os.path.join(model_dir, "meta.json"), "r", encoding="utf-8") as f:
            self.meta = json.load(f)
        self.threshold = float(self.meta.get("threshold", 0.8))

    def route(self, text, errcode=0):
        p = self.cls_route.predict_proba([text])[0]
        i = int(p.argmax())
        res = {"route": str(self.cls_route.classes_[i]),
               "confidence": round(float(p[i]), 4),
               "high_conf": bool(p[i] >= self.threshold)}
        if res["route"] == "biz":
            q = self.cls_biz.predict_proba([text])[0]
            j = int(q.argmax())
            res["biz_type"] = str(self.cls_biz.classes_[j])
            res["biz_conf"] = round(float(q[j]), 4)
            res["biz_high"] = bool(q[j] >= self.threshold)
        return res


if __name__ == "__main__":
    r = Router()
    tests = [
        "无需要发送的DAMS数据！",
        "SQLCODE:-1 SQLERRM:ORA-00001: unique constraint violated",
        "[合约=>Au9999]结算价不存在",
        "结算价这个东西怎么没有同步过来呀，是不是今天行情断了？",  # 口语化改写，考验泛化
        "平仓错误,[会员->016811][客户->0000000168][合约->Au(T+N1)][买]持仓不足,尚缺<3>",
    ]
    for t in tests:
        print(r.route(t))
