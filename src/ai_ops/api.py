# -*- coding: utf-8 -*-
"""FastAPI 薄壳（阶段 2·②）：薄封装 ai_ops.service.DiagnosticService。

定位：只加壳、不重写内核。
  - 单例服务：lifespan 启动时构建 DiagnosticService，请求经依赖注入获取；
  - 请求/响应用 pydantic 定义契约；
  - 启动：uv sync --extra api && uvicorn ai_ops.api:app --host 0.0.0.0 --port 8000
"""
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from ai_ops import reporting
from ai_ops.service import DiagnosticService

# ---------- 请求契约（pydantic） ----------


class RecordQuery(BaseModel):
    """按来源/日期/主键定位错误记录（用于 diagnose 的取数模式）。"""
    source: str | None = None
    date: str = ""
    key: dict | None = None


class DiagnoseRequest(BaseModel):
    """单条诊断：传文本（text 模式），或 source+key 从 GaussDB 取数（record 模式）。"""
    text: str | None = None
    ldate: str = ""
    errcode: int = 0
    lsection: str = ""
    record: RecordQuery | None = None
    include_report: bool = False


class BatchDiagnoseRequest(BaseModel):
    """批量诊断：items 传文本列表，或 source+date 按来源/日期全量取数。"""
    items: list[DiagnoseRequest] | None = None
    source: str | None = None
    date: str = ""


# ---------- 应用与依赖注入 ----------


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.service = DiagnosticService()
    yield


app = FastAPI(
    title="DIMPLE AIOps 诊断服务",
    description="GaussDB 报错智能诊断（规则引擎零 token 快速路径 + KB 知识卡）",
    version="0.1.0",
    lifespan=lifespan,
)


def get_service(request: Request) -> DiagnosticService:
    return request.app.state.service


# ---------- 工具 ----------


def _rec_summary(rec: dict) -> dict:
    return {
        "text": rec.get("text", ""),
        "ldate": rec.get("ldate", ""),
        "source": rec.get("source", ""),
        "source_label": rec.get("source_label", ""),
        "errcode": rec.get("errcode", 0),
        "key": rec.get("key"),
    }


def _result_summary(res: dict) -> dict:
    return {
        "class": res.get("class"),
        "type_id": (res.get("type") or {}).get("id"),
        "type_title": (res.get("type") or {}).get("title"),
        "verdict": res.get("verdict"),
        "root": res.get("root"),
        "action": res.get("action", []),
        "sql_errors": res.get("sql_errors"),
    }


# ---------- 端点 ----------


@app.get("/healthz")
def healthz(request: Request):
    """存活 + 深度自检：GaussDB 连接、规则加载数。"""
    svc = get_service(request)
    gauss = svc.check_gauss()
    return {
        "status": "ok",
        "service": "ai-ops-api",
        "gauss": {"ok": gauss["ok"], "msg": gauss["msg"]},
        "rules_count": len(svc.eng.types),
        "noise_keywords": len(svc.eng.noise_kw),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


@app.post("/v1/diagnose")
def diagnose(req: DiagnoseRequest, request: Request):
    """单条诊断：直接传报错文本，或按来源/日期/主键从 GaussDB 取数诊断。"""
    svc = get_service(request)

    if req.record and req.record.source:
        # record 模式：从 GaussDB 错误表取数
        if req.record.source not in svc.sources():
            raise HTTPException(404, "未知错误来源：%s（可选：%s）"
                                % (req.record.source, "、".join(svc.sources())))
        src = svc.sources()[req.record.source]
        key = dict(req.record.key or {})
        if req.record.date and src.date_col not in key:
            key[src.date_col] = req.record.date
        rec = svc.get_record(req.record.source, key)
        if rec is None:
            raise HTTPException(404, "记录不存在：%s %s" % (req.record.source, key))
        mode = "record"
    else:
        rec = {"text": req.text or "", "ldate": req.ldate,
               "errcode": req.errcode, "lsection": req.lsection}
        mode = "text"

    if not (rec.get("text") or "").strip():
        raise HTTPException(422, "text 为空：请提供报错文本或有效的取数主键")

    res = svc.diagnose(rec)
    out = {
        "mode": mode,
        "record": _rec_summary(rec),
        "result": res,
    }
    if req.include_report:
        out["report"] = reporting.render_rule(res)
    return out


@app.post("/v1/batch-diagnose")
def batch_diagnose(req: BatchDiagnoseRequest, request: Request):
    """批量诊断：items 文本列表，或 source+date 每日全量回放。"""
    svc = get_service(request)

    if req.items:
        recs = [{"text": it.text or "", "ldate": it.ldate,
                 "errcode": it.errcode, "lsection": it.lsection} for it in req.items]
        recs = [r for r in recs if r["text"].strip()]
    elif req.source and req.date:
        recs = svc.list_records(req.source, req.date)
    else:
        raise HTTPException(422, "需提供 items（文本列表）或 source+date（取数回放）")

    pairs = svc.diagnose_many(recs)
    return {
        "count": len(pairs),
        "results": [{"record": _rec_summary(r), "result": _result_summary(res)}
                    for r, res in pairs],
    }


@app.get("/v1/records")
def records(source: str, date: str, request: Request):
    """按来源/日期查询错误记录（供前端表格/调度取数）。"""
    svc = get_service(request)
    recs = svc.list_records(source, date)
    return {"count": len(recs), "records": [_rec_summary(r) for r in recs]}


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
