# -*- coding: utf-8 -*-
"""FastAPI 薄壳（阶段 2·② / D1 方案 C）：薄封装 ai_ops.service.DiagnosticService。

定位：只加壳、不重写内核。
  - 单例服务：lifespan 启动时构建 DiagnosticService，请求经依赖注入获取；
  - 请求/响应用 pydantic 定义契约，响应统一为 contract.DiagnosisResult 形状，
    不再透传 Engine 内部 dict（action→actions 等重命名在服务层完成）；
  - 默认纯规则零 token；escalate=true 且部署允许时才走可选 LLM 升级。
  - 启动：uv sync --extra api && uvicorn ai_ops.api:app --host 0.0.0.0 --port 8000
"""
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from ai_ops import reporting
from ai_ops.engine.db import DatabaseUnavailable
from ai_ops.engine.error_records import RecordKeyError
from ai_ops.service import MAX_BATCH, DiagnosticService

# ---------- 请求契约（pydantic） ----------


class RecordQuery(BaseModel):
    """按来源/日期/主键定位错误记录（用于 diagnose 的取数模式）。"""
    source: str | None = None
    date: str = ""
    key: dict | None = None


class DiagnoseRequest(BaseModel):
    """单条诊断：传文本（text 模式），或 source+key 从 GaussDB 取数（record 模式）。

    escalate：D1 方案 C 升级开关，默认 false（零 token、不检索 KB、不调 LLM）。
    """
    text: str | None = None
    ldate: str = ""
    errcode: int = 0
    lsection: str = ""
    record: RecordQuery | None = None
    include_report: bool = False
    escalate: bool = False


class BatchDiagnoseRequest(BaseModel):
    """批量诊断：items 传文本列表（逐条 escalate），或 source+date 整表回放（纯规则）。"""
    items: list[DiagnoseRequest] | None = None
    source: str | None = None
    date: str = ""


# ---------- 响应契约（对齐 contract.DiagnosisResult） ----------


class AnswerModel(BaseModel):
    root: str | None = None
    actions: list[str] = []
    confidence: float | None = None
    secondary: list[dict] = []
    evidence_note: str | None = None


class DiagnosisResultModel(BaseModel):
    text: str = ""
    errcode: int = 0
    ldate: str = ""
    loc: str = ""
    rule_res: dict | None = None
    kb_card: dict | None = None
    answer: AnswerModel | None = None
    source: str = ""
    escalated: bool = False
    telemetry: dict | None = None
    report: str | None = None


class BatchItemModel(BaseModel):
    record: dict
    result: DiagnosisResultModel | None = None
    error: str | None = None


class BatchResponseModel(BaseModel):
    count: int
    truncated: bool = False
    max_batch: int
    results: list[BatchItemModel]


# ---------- 应用与依赖注入 ----------


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.service = DiagnosticService()
    yield


app = FastAPI(
    title="DIMPLE AIOps 诊断服务",
    description="GaussDB 报错智能诊断（默认纯规则零 token，可选 LLM 升级 + KB 知识卡）",
    version="0.1.0",
    lifespan=lifespan,
)


def get_service(request: Request) -> DiagnosticService:
    return request.app.state.service


def _require_source(svc, source):
    """统一 source 校验（B5）：未知来源一律 404，杜绝 KeyError→500。"""
    sources = svc.sources()
    if source not in sources:
        raise HTTPException(404, "未知错误来源：%s（可选：%s）"
                            % (source, "、".join(sources)))
    return sources[source]


def _rec_summary(rec: dict) -> dict:
    return {
        "text": rec.get("text", ""),
        "ldate": rec.get("ldate", ""),
        "source": rec.get("source", ""),
        "source_label": rec.get("source_label", ""),
        "errcode": rec.get("errcode", 0),
        "key": rec.get("key"),
    }


def _batch_item(rec, res) -> BatchItemModel:
    """逐条结果：正常给契约 result；隔离捕获的异常给 error（B7）。"""
    if isinstance(res, dict) and res.get("_diagnose_error"):
        return BatchItemModel(record=_rec_summary(rec), error=res["_diagnose_error"])
    return BatchItemModel(record=_rec_summary(rec), result=res)


# ---------- 端点 ----------


@app.get("/healthz")
def healthz(request: Request):
    """存活 + 深度自检：GaussDB 连接、规则加载数。"""
    svc = get_service(request)
    gauss = svc.check_gauss()
    return {
        "status": "ok" if gauss["ok"] else "degraded",
        "service": "ai-ops-api",
        "gauss": {"ok": gauss["ok"], "msg": gauss["msg"]},
        "rules_count": len(svc.eng.types),
        "noise_keywords": len(svc.eng.noise_kw),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


@app.post("/v1/diagnose", response_model=DiagnosisResultModel)
def diagnose(req: DiagnoseRequest, request: Request):
    """单条诊断：默认纯规则零 token；escalate=true 且部署允许时可选 LLM 升级。"""
    svc = get_service(request)

    # D1 硬熔断：部署未启用升级能力时，escalate=true 直接 409（可审计、不静默）
    if req.escalate and not svc.escalation_allowed():
        raise HTTPException(
            409, "当前部署未启用 LLM 升级能力（config/llm.yaml allow_escalation=false），"
                 "拒绝升级；如需升级请由部署方开启允许位")

    if req.record and req.record.source:
        # record 模式：从 GaussDB 错误表取数
        src = _require_source(svc, req.record.source)
        key = dict(req.record.key or {})
        if req.record.date and src.date_col not in key:
            key[src.date_col] = req.record.date
        try:
            rec = svc.get_record(req.record.source, key)
        except RecordKeyError as e:
            raise HTTPException(422, str(e))
        except DatabaseUnavailable as e:
            raise HTTPException(503, str(e))
        if rec is None:
            raise HTTPException(404, "记录不存在：%s %s" % (req.record.source, key))
    else:
        rec = {"text": req.text or "", "ldate": req.ldate,
               "errcode": req.errcode, "lsection": req.lsection}

    if not (rec.get("text") or "").strip():
        raise HTTPException(422, "text 为空：请提供报错文本或有效的取数主键")

    if req.escalate:
        out = svc.diagnose_escalated(rec)  # LLM 不可用时内部已优雅降级，200 返回
    else:
        out = svc.diagnose_rule_only(rec)

    if req.include_report:
        # 纯规则/升级路径的 rule_res 都可渲染为文本报告
        out["report"] = reporting.render_rule(out["rule_res"])
    return out


@app.post("/v1/batch-diagnose", response_model=BatchResponseModel)
def batch_diagnose(req: BatchDiagnoseRequest, request: Request):
    """批量诊断：items 支持逐条 escalate；source+date 整表回放始终纯规则。"""
    svc = get_service(request)
    truncated = False

    if req.items:
        recs, flags = [], []
        for it in req.items:
            # 任一条目要求升级而部署不允许 → 整体 409（显式、可审计）
            if it.escalate and not svc.escalation_allowed():
                raise HTTPException(
                    409, "当前部署未启用 LLM 升级能力，条目 %s 的 escalate=true 被拒绝"
                         % (it.text or "")[:40])
            recs.append({"text": it.text or "", "ldate": it.ldate,
                         "errcode": it.errcode, "lsection": it.lsection})
            flags.append(it.escalate)
        keep = [i for i, r in enumerate(recs) if r["text"].strip()]
        recs = [recs[i] for i in keep]
        flags = [flags[i] for i in keep]
    elif req.source and req.date:
        _require_source(svc, req.source)
        # 整表回放：纯规则、不做 LLM 扇出；取数带上限（+1 探测截断）
        try:
            recs = svc.list_records(req.source, req.date, limit=MAX_BATCH + 1)
        except DatabaseUnavailable as e:
            raise HTTPException(503, str(e))
        if len(recs) > MAX_BATCH:
            recs = recs[:MAX_BATCH]
            truncated = True
        flags = None
    else:
        raise HTTPException(422, "需提供 items（文本列表）或 source+date（取数回放）")

    pairs = svc.diagnose_many_isolated(recs, escalate_flags=flags)
    return BatchResponseModel(
        count=len(pairs), truncated=truncated, max_batch=MAX_BATCH,
        results=[_batch_item(r, res) for r, res in pairs])


@app.get("/v1/records")
def records(source: str, date: str, request: Request, limit: int | None = None):
    """按来源/日期查询错误记录（供前端表格/调度取数）；limit 有硬上限，默认封顶。"""
    svc = get_service(request)
    _require_source(svc, source)
    eff_limit = MAX_BATCH if limit is None else max(1, min(limit, MAX_BATCH))
    try:
        recs = svc.list_records(source, date, limit=eff_limit)
    except DatabaseUnavailable as e:
        raise HTTPException(503, str(e))
    return {"count": len(recs), "limit": eff_limit,
            "records": [_rec_summary(r) for r in recs]}


@app.get("/v1/rules")
def rules(request: Request):
    """规则清单（类型/runbook/关键词）；覆盖率由 scripts/coverage_scan.py 离线扫描。"""
    svc = get_service(request)
    items = [{
        "id": t.get("id"),
        "title": t.get("title"),
        "runbook": t.get("runbook"),
        "keywords": t.get("keywords", []),
        "err_codes": t.get("err_codes", []),
    } for t in svc.eng.types]
    return {
        "total": len(items),
        "noise_keywords": svc.eng.noise_kw,
        "rules": items,
        "coverage": "覆盖率由 scripts/coverage_scan.py 离线扫描（口径：7 张历史表全量条数为分母、TOP200 骨架命中为分子）",
    }
