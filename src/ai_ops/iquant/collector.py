# -*- coding: utf-8 -*-
"""iQuant 实时采集器（接口级，拉模式）。

与 DimpleCollector 同构，按 iQuant 平台的实际数据结构做了适配：
  - 单端点：事中风控「日间异常风控事件」queryTable，覆盖 7 类风控项；
  - 分页：请求体 {pageNo, pageSize, data:{...}}，返回顶层 data/total，成功码 200000；
  - 时间为 ISO 字符串（2026-11-20T09:25:48.377），转业务日期 YYYYMMDD；
  - triggerValue/thresholdValue/controlAction 为 JSON 字符串，二次解析后保留；
  - 增量指纹只基于稳定主键 eventId（事件会随 triggerCount 更新，不能纳入易变文本），
    同一事件只诊断一次；
  - 默认只处理未闭环事件（NEW/NOTIFIED），HANDLED/IGNORED 标记后跳过。

诊断复用 DiagnosticService，落库 best-effort，单端点异常隔离，不影响调度器与其他任务。
"""
import hashlib
import json
import logging
from collections import namedtuple
from datetime import datetime

from .client import IquantClient, IquantError
from ..config import load_config
from ..paths import state_file
from ..service import DiagnosticService

logger = logging.getLogger(__name__)

# 未闭环状态：实时监控只诊断这些；已处理/已忽略的事件不再重复诊断。
DEFAULT_OPEN_STATUSES = ("NEW", "NOTIFIED")

# 端点定义（保留注册表结构，便于后续接入更多 iQuant 事件接口）。
Endpoint = namedtuple(
    "Endpoint",
    ["id", "label", "path", "key_col", "time_col", "extra_filters"])

ENDPOINTS = [
    Endpoint(
        id="iquant_day_abnormal_event",
        label="iQuant事中风控事件",
        path="/risk/dayAbnormalRiskEvent/queryTable",
        key_col="eventId",
        time_col="lastTriggerTime",
        extra_filters={},
    ),
]

# 风控项代码 -> 中文名（与存量 935 条事件枚举一致）。
RISK_ITEM_CN = {
    "QUOTE_MARKET_DEVIATION": "在市报价市场偏离",
    "POSITION_SWING": "交易头寸大幅波动",
    "MANUAL_PRICE_CHANGE": "手动修改报价",
    "ISSUER_CONCENTRATION": "单一发行主体持仓集中度",
    "BULK_CLICK_DEAL": "报价被批量点击成交",
    "SPECIAL_TRADE_MONITOR": "特定类型交易监控",
    "DEAL_TYPE_ABNORMAL": "成交类型异常",
}

RISK_LEVEL_CN = {"LOW": "低", "MEDIUM": "中", "HIGH": "高"}

EVENT_STATUS_CN = {
    "NEW": "新建", "NOTIFIED": "已通知",
    "HANDLED": "已处理", "IGNORED": "已忽略",
}

# ---------------- 配置 ----------------

_DEFAULTS = {
    "enabled": False,
    "base_url": "http://10.242.184.55:1080",
    "username": "admin",
    "password": "",
    "client_id": "testjwtclientid",
    "client_secret": "XY7kmzoNzl100",
    "timeout": 10,
    "interval_minutes": 5,
    "page_size": 100,
    "max_pages": 200,
    "handle_closed": False,
    "open_statuses": list(DEFAULT_OPEN_STATUSES),
}

def load_iquant_config():
    """读取 iquant 配置并补默认值（环境变量覆盖在 config.load_config 内完成）。"""
    out = dict(_DEFAULTS)
    out.update(load_config("iquant"))
    return out


def is_enabled(cfg=None):
    """实时监控总开关，缺省关闭。"""
    cfg = cfg or load_iquant_config()
    return bool(cfg.get("enabled", False))


def build_client(cfg=None):
    cfg = cfg or load_iquant_config()
    return IquantClient(
        base_url=cfg["base_url"],
        username=cfg["username"],
        password=cfg["password"],
        client_id=cfg.get("client_id") or "testjwtclientid",
        client_secret=cfg.get("client_secret") or "XY7kmzoNzl100",
        timeout=cfg.get("timeout", 10),
    )


# ---------------- 字段映射 ----------------

def _maybe_json(value):
    """JSON 字符串则解析为对象，否则原样返回（解析失败也原样返回）。"""
    if not isinstance(value, str):
        return value
    s = value.strip()
    if s and s[0] in "{[":
        try:
            return json.loads(s)
        except json.JSONDecodeError:
            return value
    return value


def _compact(value):
    """把解析后的对象压成紧凑、不转义中文的 JSON 文本，用于诊断文本。"""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _parse_iso_date(value):
    """ISO 时间（2026-11-20T09:25:48.377）-> 业务日期 20261120；无法解析返回空串。"""
    if not value:
        return ""
    return str(value)[:10].replace("-", "")


def _render_text(raw, params):
    """渲染供诊断内核使用的可读中文文本，保留规则、级别、对象、命中详情等关键信息。"""
    risk_item = raw.get("riskItem")
    risk_level = raw.get("riskLevel")
    event_status = raw.get("eventStatus")
    parts = [
        "事中风控告警：%s（规则编号 %s）"
        % (raw.get("ruleName") or "", raw.get("ruleNo") or ""),
        "风控项 %s" % RISK_ITEM_CN.get(risk_item, risk_item or ""),
        "风险级别 %s" % RISK_LEVEL_CN.get(risk_level, risk_level or ""),
        "事件状态 %s" % EVENT_STATUS_CN.get(event_status, event_status or ""),
    ]
    for col, label in (("objectName", "触发对象"), ("productScope", "产品"),
                       ("portfolioScope", "投组"), ("traderScope", "交易员")):
        if raw.get(col):
            parts.append("%s %s" % (label, raw.get(col)))

    trigger = params.get("triggerValueParsed")
    if trigger not in (None, "", [], {}):
        parts.append("命中详情 %s" % _compact(trigger))
    threshold = params.get("thresholdValueParsed")
    if threshold not in (None, "", [], {}):
        parts.append("阈值 %s" % _compact(threshold))
    actions = params.get("controlActionParsed")
    if actions:
        parts.append("管控动作 %s" % _compact(actions))
    if raw.get("triggerCount"):
        parts.append("触发次数 %s" % raw.get("triggerCount"))
    if raw.get("lastTriggerTime"):
        parts.append("最近触发 %s" % raw.get("lastTriggerTime"))
    return "，".join(parts)


def normalize_record(raw, ep):
    """把 iQuant 原始事件映射为诊断内核标准记录（与 dimple 输出结构一致）。"""
    raw = raw or {}
    params = dict(raw)
    # 嵌套 JSON 字符串二次解析，保留原字段的同时提供 *Parsed 版本。
    for col in ("triggerValue", "thresholdValue", "controlAction"):
        if col in params:
            params[col + "Parsed"] = _maybe_json(params[col])

    ldate = _parse_iso_date(raw.get(ep.time_col) or raw.get("firstTriggerTime"))
    key = {ep.key_col: raw.get(ep.key_col)}
    return {
        "text": _render_text(raw, params),
        "ldate": ldate,
        "errcode": 0,
        "lsection": "",
        "source": ep.id,
        "source_label": ep.label,
        "key": key,
        "params": params,
    }


def _event_fingerprint(ep, event_id):
    """基于稳定主键 eventId 的增量指纹。

    事件会随 triggerCount/lastTriggerTime 更新而文本变化，故指纹不纳入文本，
    保证同一 eventId 全局只诊断、落库一次。
    """
    return hashlib.sha256(
        ("iquant:%s:%s" % (ep.id, event_id)).encode("utf-8")).hexdigest()


# ---------------- 游标（增量幂等） ----------------

class CursorStore:
    """本地游标：记录已处理事件指纹，重启不丢，自动清理过期指纹。"""

    def __init__(self, path=None, ttl_days=30):
        self.path = path or state_file("iquant_cursor")
        self.ttl_days = ttl_days
        self._seen = {}
        self._load()

    def _load(self):
        if not self.path.exists():
            return
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            self._seen = dict(payload.get("seen", {}))
        except (json.JSONDecodeError, OSError) as e:
            logger.warning("iQuant 游标读取失败，按空游标启动：%s", e)
            self._seen = {}
        self._prune()

    def _prune(self):
        cutoff = datetime.now().timestamp() - self.ttl_days * 86400
        before = len(self._seen)
        self._seen = {fp: ts for fp, ts in self._seen.items() if ts >= cutoff}
        if len(self._seen) != before:
            logger.info("iQuant 游标清理过期指纹 %d 条", before - len(self._seen))

    def seen(self, fingerprint):
        return fingerprint in self._seen

    def mark(self, fingerprint):
        self._seen[fingerprint] = datetime.now().timestamp()

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".json.tmp")
        tmp.write_text(
            json.dumps({"seen": self._seen}, ensure_ascii=False, indent=2),
            encoding="utf-8")
        tmp.replace(self.path)


# ---------------- 实时采集主流程 ----------------

def run_realtime_collection(svc=None, client=None, *, cursor=None, max_pages=None):
    """拉取全部端点的增量事件并诊断落库，返回汇总 dict。"""
    cfg = load_iquant_config()
    if not is_enabled(cfg):
        return {"status": "disabled", "source": "iquant"}

    summary = {
        "status": "ok",
        "source": "iquant",
        "batch_id": datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3],
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "fetched": 0,
        "skipped_seen": 0,
        "skipped_closed": 0,
        "diagnosed": 0,
        "errors": 0,
        "by_endpoint": {},
    }

    client = client or build_client(cfg)
    cursor = cursor or CursorStore()
    svc = svc or DiagnosticService()
    open_statuses = set(cfg.get("open_statuses") or DEFAULT_OPEN_STATUSES)
    handle_closed = bool(cfg.get("handle_closed", False))
    page_size = int(cfg.get("page_size", 100))
    cap = int(max_pages or cfg.get("max_pages", 200))

    try:
        for ep in ENDPOINTS:
            ep_stat = {"fetched": 0, "skipped_seen": 0, "skipped_closed": 0,
                       "diagnosed": 0, "errors": 0}
            summary["by_endpoint"][ep.id] = ep_stat
            pending = []  # [(标准记录, 指纹)]
            try:
                page_no = 1
                while page_no <= cap:
                    out = client.query_page(
                        ep.path, page_no, page_size,
                        filters=dict(ep.extra_filters))
                    rows = out.get("data") or []
                    if not rows:
                        break
                    for raw in rows:
                        summary["fetched"] += 1
                        ep_stat["fetched"] += 1
                        event_id = raw.get(ep.key_col)
                        fp = _event_fingerprint(ep, event_id)
                        if event_id is None or cursor.seen(fp):
                            summary["skipped_seen"] += 1
                            ep_stat["skipped_seen"] += 1
                            continue
                        # 已闭环事件默认不诊断，仅标记指纹避免后续重复判断。
                        if not handle_closed and raw.get("eventStatus") not in open_statuses:
                            cursor.mark(fp)
                            summary["skipped_closed"] += 1
                            ep_stat["skipped_closed"] += 1
                            continue
                        pending.append((normalize_record(raw, ep), fp))

                    total = int(out.get("total") or 0)
                    total_pages = max(1, (total + page_size - 1) // page_size)
                    if page_no >= total_pages:
                        break
                    page_no += 1
            except IquantError as e:
                ep_stat["errors"] += 1
                summary["errors"] += 1
                logger.error("iQuant 端点 %s 拉取失败：%s", ep.id, e)

            # 诊断：逐条隔离 + 内部 best-effort 自动 upsert 落库（与 dimple 同款）。
            if not pending:
                continue
            ctx = {"trigger_type": "scheduled", "batch_id": summary["batch_id"]}
            recs = [rec for rec, _ in pending]
            fp_by_id = {id(rec): fp for rec, fp in pending}
            try:
                diagnosed = svc.diagnose_many_isolated(recs, _ctx=ctx)
            except Exception as e:
                # 防御性兜底：正常情况下单条异常已在服务内部隔离，不会走到这里。
                logger.error("iQuant 端点 %s 整批诊断失败：%s", ep.id, e)
                ep_stat["errors"] += len(pending)
                summary["errors"] += len(pending)
                for _, fp in pending:
                    cursor.mark(fp)
                continue

            for rec, result in diagnosed:
                if isinstance(result, dict) and result.get("_diagnose_error"):
                    ep_stat["errors"] += 1
                    summary["errors"] += 1
                else:
                    ep_stat["diagnosed"] += 1
                    summary["diagnosed"] += 1
                # 诊断完成后再标记游标，异常条目也标记，避免下轮反复重试同一条。
                cursor.mark(fp_by_id[id(rec)])
    finally:
        cursor.save()
        close = getattr(svc, "close", None)
        if callable(close):
            try:
                close()
            except Exception:
                pass

    summary["finished_at"] = datetime.now().isoformat(timespec="seconds")
    return summary
