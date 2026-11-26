# -*- coding: utf-8 -*-
"""iQuant 实时采集器（接口级，拉模式）。

与 DimpleCollector 同构，按 iQuant 平台的实际数据结构做了适配：
  - 单端点：事中风控「日间异常风控事件」queryTable，覆盖 7 类风控项；
  - 分页：请求体 {pageNo, pageSize, data:{...}}，返回顶层 data/total，成功码 200000；
  - 时间为 ISO 字符串（2026-11-20T09:25:48.377），转业务日期 YYYYMMDD；
  - triggerValue/thresholdValue/controlAction 为 JSON 字符串，二次解析后保留；
  - 增量指纹只基于稳定主键 eventId（事件会随 triggerCount 更新，不能纳入易变文本），
    同一事件只诊断一次；仅诊断且要求的落库成功后推进游标，失败留待下轮重试；
  - 默认只处理未闭环事件（NEW/NOTIFIED），HANDLED/IGNORED 跳过但不写游标，
    后续开启 handle_closed 可补采；游标默认永久保留，避免历史事件过期重放；
  - 达到 max_pages 硬上限时持久化下轮起始页，跨轮推进直至扫完，并通过
    summary.truncated 与告警日志显式报告；
  - 游标文件附带的跨进程锁避免多 API worker 重复采集与并发写游标。

诊断复用 DiagnosticService，落库 best-effort，单端点异常隔离，不影响调度器与其他任务。
"""
import errno
import hashlib
import json
import logging
import os
from collections import namedtuple
from datetime import datetime

from ..config import load_config
from ..paths import state_file
from ..service import DiagnosticService
from .client import IquantClient, IquantError

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

class CursorStoreError(Exception):
    """游标读取/结构损坏；必须中止采集，不能按空游标重放历史事件。"""


class CursorStore:
    """本地游标：成功事件指纹 + 截断时的下轮起始页，重启不丢。

    默认永久保留指纹：上游仍返回历史事件时，过期删除会造成重复诊断、upsert
    覆盖人工标注。仅当部署明确接受该重放风险时才设置 ttl_days 做容量清理。
    诊断/落库失败与按配置跳过的闭环事件均不写入，留待后续轮次重新判断。
    """

    def __init__(self, path=None, ttl_days=None):
        self.path = path or state_file("iquant_cursor")
        self.ttl_days = ttl_days
        self._seen = {}
        self._positions = {}
        self._load()

    def reload(self):
        """获得跨进程锁后重读，避免使用拿锁前加载的过期状态。"""
        self._seen = {}
        self._positions = {}
        self._load()

    def _load(self):
        if not self.path.exists():
            return
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict) or not isinstance(payload.get("seen"), dict):
                raise ValueError("游标结构必须为 {'seen': {...}, 'positions': {...}}")
            positions = payload.get("positions") or {}
            if not isinstance(positions, dict):
                raise ValueError("游标 positions 必须为对象")
            # 非数字时间戳/页码按损坏条目丢弃，不让单个字段拖垮状态解析。
            self._seen = {
                str(fp): float(ts) for fp, ts in payload["seen"].items()
                if isinstance(ts, (int, float)) and not isinstance(ts, bool)}
            self._positions = {
                str(ep): int(page) for ep, page in positions.items()
                if isinstance(page, int) and not isinstance(page, bool) and page > 1}
        except (json.JSONDecodeError, OSError, ValueError, TypeError) as e:
            self._seen = {}
            self._positions = {}
            raise CursorStoreError("iQuant 游标读取失败：%s" % e) from e
        self._prune()

    def _prune(self):
        if not self.ttl_days:
            return
        cutoff = datetime.now().timestamp() - self.ttl_days * 86400
        before = len(self._seen)
        self._seen = {fp: ts for fp, ts in self._seen.items() if ts >= cutoff}
        if len(self._seen) != before:
            logger.info("iQuant 游标清理过期指纹 %d 条", before - len(self._seen))

    def seen(self, fingerprint):
        return fingerprint in self._seen

    def mark(self, fingerprint):
        self._seen[fingerprint] = datetime.now().timestamp()

    def next_page(self, endpoint_id):
        """本轮起始页；正常完成一轮全量扫描后回到第 1 页。"""
        return self._positions.get(endpoint_id, 1)

    def set_next_page(self, endpoint_id, page_no):
        if page_no <= 1:
            self._positions.pop(endpoint_id, None)
        else:
            self._positions[endpoint_id] = int(page_no)

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".json.tmp")
        tmp.write_text(
            json.dumps({"seen": self._seen, "positions": self._positions},
                       ensure_ascii=False, indent=2),
            encoding="utf-8")
        tmp.replace(self.path)


# ---------------- 跨进程互斥 ----------------

class _InterProcessLock:
    """基于文件的非阻塞跨进程锁（Windows msvcrt / POSIX flock）。

    多 Uvicorn worker 都会注册进程内调度 job；此锁保证同一游标文件对应的
    采集同一时刻只在一个进程执行，避免重复请求/诊断与临时游标文件互相覆盖。
    锁文件保留不删除，句柄关闭或进程退出即自动释放。
    """

    def __init__(self, path):
        self.path = path
        self._fh = None

    def acquire(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fh = open(self.path, "a+b")
        try:
            if os.name == "nt":
                import msvcrt
                # Windows locking 需要一个实际存在的字节区间。
                fh.seek(0, os.SEEK_END)
                if fh.tell() == 0:
                    fh.write(b"0")
                    fh.flush()
                fh.seek(0)
                msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as e:
            fh.close()
            conflicts = {errno.EACCES, errno.EAGAIN, errno.EWOULDBLOCK,
                         errno.EDEADLK, getattr(errno, "EDEADLOCK", errno.EDEADLK)}
            if e.errno in conflicts:
                return False
            # ENOTSUP、句柄耗尽、I/O 错误等不是锁竞争，必须暴露而非假装被占用。
            raise
        self._fh = fh
        return True

    def release(self):
        fh, self._fh = self._fh, None
        if fh is None:
            return
        try:
            if os.name == "nt":
                import msvcrt
                fh.seek(0)
                msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        except OSError:
            pass
        finally:
            fh.close()


# ---------------- 实时采集主流程 ----------------

def run_realtime_collection(svc=None, client=None, *, cursor=None, max_pages=None):
    """拉取全部端点的增量事件并诊断落库，返回汇总 dict。"""
    cfg = load_iquant_config()
    if not is_enabled(cfg):
        return {"status": "disabled", "source": "iquant"}

    cursor_path = cursor.path if cursor is not None else state_file("iquant_cursor")
    lock = _InterProcessLock(
        cursor_path.with_name(cursor_path.name + ".lock"))
    if not lock.acquire():
        logger.info("iQuant 实时采集已由另一进程执行，本轮跳过")
        return {"status": "locked", "source": "iquant"}
    try:
        # 必须先持锁再加载/重载；否则另一个 worker 可能用过期的空游标重放并覆盖新状态。
        if cursor is None:
            cursor = CursorStore(path=cursor_path)
        else:
            cursor.reload()
    except CursorStoreError as e:
        logger.error("iQuant 游标不可用，本轮中止以避免重放历史事件：%s", e)
        lock.release()
        return {"status": "error", "source": "iquant",
                "error": "cursor_load_failed", "message": str(e)}

    summary = {
        "status": "ok",
        "source": "iquant",
        "batch_id": datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3],
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "fetched": 0,
        "skipped_seen": 0,
        "skipped_closed": 0,
        "invalid": 0,
        "diagnosed": 0,
        "errors": 0,
        "truncated": False,
        "by_endpoint": {},
    }

    open_statuses = set(cfg.get("open_statuses") or DEFAULT_OPEN_STATUSES)
    handle_closed = bool(cfg.get("handle_closed", False))
    page_size = int(cfg.get("page_size", 100))
    cap = max(1, int(max_pages or cfg.get("max_pages", 200)))

    try:
        client = client or build_client(cfg)
        svc = svc or DiagnosticService()
        for ep in ENDPOINTS:
            ep_stat = {"fetched": 0, "skipped_seen": 0, "skipped_closed": 0,
                       "invalid": 0, "diagnosed": 0, "errors": 0,
                       "total": 0, "truncated": False}
            summary["by_endpoint"][ep.id] = ep_stat
            pending = []  # [(标准记录, 指纹)]
            total = 0
            start_page = cursor.next_page(ep.id)
            page_no = start_page
            pages_fetched = 0
            ep_stat["page_start"] = start_page
            try:
                while pages_fetched < cap:
                    out = client.query_page(
                        ep.path, page_no, page_size,
                        filters=dict(ep.extra_filters))
                    pages_fetched += 1
                    if not isinstance(out, dict):
                        raise IquantError("接口响应不是 JSON 对象")
                    rows = out.get("data") or []
                    if not isinstance(rows, list):
                        raise IquantError("接口响应 data 不是数组")
                    if not rows:
                        # 起始页已超过当前结果集（数据归档/收缩），下轮回第 1 页。
                        cursor.set_next_page(ep.id, 1)
                        break
                    try:
                        total = int(out.get("total") or 0)
                    except (TypeError, ValueError) as e:
                        raise IquantError("接口响应 total 不是数字") from e
                    for raw in rows:
                        summary["fetched"] += 1
                        ep_stat["fetched"] += 1
                        if not isinstance(raw, dict):
                            summary["invalid"] += 1
                            ep_stat["invalid"] += 1
                            continue
                        event_id = raw.get(ep.key_col)
                        if event_id in (None, ""):
                            # 缺稳定主键不能指纹去重，也不能静默归入 skipped_seen。
                            summary["invalid"] += 1
                            ep_stat["invalid"] += 1
                            continue
                        fp = _event_fingerprint(ep, event_id)
                        if cursor.seen(fp):
                            summary["skipped_seen"] += 1
                            ep_stat["skipped_seen"] += 1
                            continue
                        # 已闭环事件默认不诊断；不写游标，后续开启 handle_closed
                        # 或调整 open_statuses 后仍能重新纳入，而不是被永久跳过。
                        if not handle_closed and raw.get("eventStatus") not in open_statuses:
                            summary["skipped_closed"] += 1
                            ep_stat["skipped_closed"] += 1
                            continue
                        pending.append((normalize_record(raw, ep), fp))

                    total_pages = max(1, (total + page_size - 1) // page_size)
                    if page_no >= total_pages:
                        cursor.set_next_page(ep.id, 1)
                        break
                    page_no += 1
                else:
                    # 本轮到上限但保存下一页，后续轮次推进直至扫完，而非永远重复前 N 页。
                    cursor.set_next_page(ep.id, page_no)
                    ep_stat["truncated"] = True
                    summary["truncated"] = True
                    logger.warning(
                        "iQuant 端点 %s 本轮达到 max_pages=%d 上限（total=%d），"
                        "下轮将从第 %d 页继续",
                        ep.id, cap, total, page_no)
            except IquantError as e:
                ep_stat["errors"] += 1
                summary["errors"] += 1
                logger.error("iQuant 端点 %s 拉取失败：%s", ep.id, e)
            ep_stat["total"] = total
            ep_stat["page_next"] = cursor.next_page(ep.id)
            if ep_stat["invalid"]:
                logger.warning(
                    "iQuant 端点 %s 有 %d 条非对象或缺少稳定主键 %s 的记录，已跳过",
                    ep.id, ep_stat["invalid"], ep.key_col)

            # 诊断：逐条隔离 + 内部 best-effort 自动 upsert 落库（与 dimple 同款）。
            if not pending:
                continue
            ctx = {"trigger_type": "scheduled", "batch_id": summary["batch_id"]}
            recs = [rec for rec, _ in pending]
            fp_by_id = {id(rec): fp for rec, fp in pending}
            try:
                diagnosed = svc.diagnose_many_isolated(recs, _ctx=ctx)
            except Exception as e:
                # 防御性兜底：整批失败不推进任何游标，恢复后整批重试。
                logger.error("iQuant 端点 %s 整批诊断失败：%s", ep.id, e)
                ep_stat["errors"] += len(pending)
                summary["errors"] += len(pending)
                continue

            for rec, result in diagnosed:
                diagnose_error = isinstance(result, dict) and result.get("_diagnose_error")
                persist_error = isinstance(result, dict) and result.get("_persist_error")
                if diagnose_error or persist_error:
                    # 临时故障不能造成永久漏诊断/漏落库：失败条目保持未见，下轮重试。
                    ep_stat["errors"] += 1
                    summary["errors"] += 1
                    continue
                ep_stat["diagnosed"] += 1
                summary["diagnosed"] += 1
                # 仅在诊断且要求的落库成功后推进游标。
                cursor.mark(fp_by_id[id(rec)])
    finally:
        try:
            cursor.save()
            close = getattr(svc, "close", None)
            if callable(close):
                try:
                    close()
                except Exception:
                    pass
        finally:
            lock.release()

    summary["finished_at"] = datetime.now().isoformat(timespec="seconds")
    return summary
