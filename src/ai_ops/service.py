# -*- coding: utf-8 -*-
"""诊断服务层（阶段 2·①）：把业务逻辑从 Streamlit 页面收敛到独立模块。

定位：
  - 纯 Python，零 UI 依赖（不 import streamlit）；
  - 页面（demo/app.py）、CLI 与未来的 FastAPI 共用同一服务面；
  - 只做编排，不改诊断逻辑（内核行为不变，纯重构）。

组件：
  - Engine / KnowledgeClient 默认自建，可注入复用
    （服务化时 FastAPI 用依赖注入，页面用 st.cache_resource 缓存实例）；
  - 取数委托 ai_ops.engine.error_records（GaussDB 7 张错误历史表）。
"""
from datetime import datetime
from socket import create_connection

from ai_ops.config import load_config
from ai_ops.engine import error_records as ER
from ai_ops.engine.rule_engine import Engine
from ai_ops.kb.client import KnowledgeClient

# 真实记录演示（页①，从 GaussDB 错误表取数）
REAL_DEMOS = [
    ("演示① 敞口不够（GaussDB 真实记录）", "exposure",
     {"trade_date": "20250304", "trader_no": "trader",
      "local_no": "000000000001", "purpose_code": "ZY"}),
    ("演示③ 平仓数量不够（GaussDB 真实记录）", "close_posi",
     {"trade_date": "20250321", "trader_no": "trader9",
      "local_no": "000000000006", "purpose_code": "ZY"}),
    ("演示④ 策略资金不足（GaussDB 真实记录，最高频）", "fund",
     {"trade_date": "20250321", "trader_no": "trader1",
      "local_no": "000000240421", "purpose_code": "ZY"}),
]


def build_engine():
    return Engine()


def build_kb():
    return KnowledgeClient()


class DiagnosticService:
    """诊断服务：取数 → 诊断 → 证据增强；页面 / CLI / API 共用同一服务面。"""

    def __init__(self, eng=None, kb=None):
        self.eng = eng if eng is not None else build_engine()
        self.kb = kb if kb is not None else build_kb()

    # ---- 取数（委托 error_records，GaussDB 7 来源）----

    def sources(self):
        return ER.SOURCES

    def get_record(self, source, key):
        """按来源主键取单条错误记录；无结果返回 None。"""
        return ER.get_record(source, key)

    def list_records(self, source, date):
        """按来源/日期取错误记录列表（仅文本非空）。"""
        return ER.list_records(source, date)

    def demo_record(self, key):
        """按演示 key 取对应真实错误记录（页①一键演示）。"""
        for _label, _key, d in REAL_DEMOS:
            if _key == key:
                return ER.get_record("ftr_err", d)
        return None

    # ---- 诊断（委托规则引擎）----

    def diagnose(self, rec):
        return self.eng.diagnose(rec)

    def diagnose_many(self, recs):
        """批量诊断，返回 [(record, result), ...]。"""
        return [(r, self.eng.diagnose(r)) for r in recs]

    # ---- 证据增强（KB 知识卡）----

    def kb_card(self, text):
        """知识库机制卡；知识库不可用时返回 None（静默降级）。"""
        if not self.kb.available():
            return None
        return self.kb.diagnose_card(text)

    # ---- 环境预检 ----

    @staticmethod
    def check_gauss(timeout=1.5):
        """GaussDB TCP 预检（host/port），返回 {ok, msg, checked}。"""
        cfg = load_config("db")
        host, port = cfg.get("host"), int(cfg.get("port") or 0)
        try:
            with create_connection((host, port), timeout=timeout):
                ok = True
                msg = "%s:%s 可达（库 %s）" % (host, port, cfg.get("database"))
        except OSError as e:
            ok = False
            msg = "%s:%s 不可达（%s）" % (host, port, type(e).__name__)
        return {"ok": ok, "msg": msg, "checked": datetime.now().strftime("%H:%M:%S")}
