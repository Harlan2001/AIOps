# -*- coding: utf-8 -*-
"""规则引擎（运行时零模型）：正则解析 -> 类型匹配 -> 参数化只读 SQL 诊断树 -> 结构化结论。"""
import re
from collections import defaultdict

from ai_ops import rules_store
from ai_ops.engine import parser as P
from ai_ops.engine.db import get_conn

_BIND_RE = re.compile(r":(\w+)")


class Engine:
    def __init__(self):
        self.types, self.noise_kw = rules_store.load_registries()
        self._runbooks = {}
        self._conn = None

    def _classify(self, text, errcode):
        """ora / other / biz 判定用解析器通用规则；噪音判定由 noise_rules.yaml 驱动。"""
        if P.is_ora(text):
            return "ora"
        if not P.is_chinese(text):
            return "other"
        if any(k in text for k in P.ERROR_KW):
            return "biz"
        if errcode and errcode != 0:
            return "biz"
        if any(k in text for k in self.noise_kw):
            return "noise"
        return "other"

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def _conn_get(self):
        if self._conn is None:
            self._conn = get_conn()
        return self._conn

    def _load_runbook(self, name):
        if name not in self._runbooks:
            self._runbooks[name] = rules_store.load_runbook(name)
        return self._runbooks[name]

    def match_type(self, text, errcode):
        """关键词命中为必要条件（错误码在不同业务场景会被复用，不能单独决定类型）；
        错误码仅用于关键词命中后的排序。"""
        best, best_score = None, 0
        for t in self.types:
            kw_hits = sum(1 for kw in t.get("keywords", []) if kw in text)
            if kw_hits == 0:
                continue
            score = kw_hits * 10
            if errcode and errcode in t.get("err_codes", []):
                score += 2
            if score > best_score:
                best, best_score = t, score
        return best, best_score

    def _build_params(self, raw, ldate, type_cfg, rb):
        rawp = P.extract_params(raw)
        alias = type_cfg.get("param_alias", {})
        params = {}
        for cn, val in rawp.items():
            params[alias.get(cn, cn)] = val
        # 默认诊断日期 = 日志日期
        params["trade_date"] = ldate[:10].replace("-", "") if ldate else ""
        # 额外参数（从原文正则）
        for name, cfg in (rb.get("extra_params") or {}).items():
            m = re.search(cfg["regex"], raw)
            if m:
                params[name] = m.group(1)
        # 日期覆盖（如从成交编号提取业务日期）
        df = rb.get("date_from")
        if df:
            src = params.get(df["field"])
            if src:
                m = re.search(df["regex"], src)
                if m:
                    params["trade_date"] = m.group(1)
        return params

    def _run_sql(self, sql, params):
        need = set(_BIND_RE.findall(sql))
        present = {k for k, v in params.items() if v not in (None, "")}
        missing = need - present
        if missing:
            return {"status": "missing_params", "missing": sorted(missing)}
        b = {k: params[k] for k in need}
        cur = self._conn_get().cursor()
        cur.execute(sql, b)
        cols = [d[0] for d in cur.description]
        rows = [list(r) for r in cur.fetchall()]
        return {"status": "ok", "cols": cols, "rows": rows}

    @staticmethod
    def _fmt(tpl, params):
        if not tpl:
            return ""
        return tpl.format_map(defaultdict(lambda: "（缺失）", params))

    def diagnose(self, record):
        text = (record.get("text") or "").strip()
        errcode = record.get("errcode") or 0
        ldate = record.get("ldate") or ""
        lsection = record.get("lsection") or ""
        res = {
            "class": self._classify(text, errcode), "text": text, "errcode": errcode,
            "ldate": ldate, "lsection": lsection, "loc": P.parse_lsection(lsection),
        }

        if res["class"] == "noise":
            res["verdict"] = "非故障提示（定时任务成功/无数据流水），无需诊断"
            return res
        if res["class"] == "ora":
            res["verdict"] = "Oracle 技术错误（本期不诊断，建议转 DBA）"
            return res
        if res["class"] == "other":
            res["verdict"] = "未识别类型，进入通用兜底 / 回流待补规则"
            return res

        tcfg, score = self.match_type(text, errcode)
        if not tcfg:
            res["verdict"] = "业务报错但未匹配规则，进入兜底 / 回流待补规则"
            return res

        rb = self._load_runbook(tcfg["runbook"])
        params = self._build_params(text, ldate, tcfg, rb)
        res.update({"type": tcfg, "runbook": rb["id"], "params": params, "evidence": []})

        # 跑完所有检查，收集全部失败项，再按"主检查优先"综合判定
        failures = []
        for step in rb["steps"]:
            r = self._run_sql(step["sql"], params)
            ev = {"id": step["id"], "title": step.get("title"), "kind": step["type"], "r": r}
            res["evidence"].append(ev)
            if step["type"] == "sql_check" and r["status"] == "ok":
                exists = len(r["rows"]) > 0
                want = step.get("expect", {}).get("exists", True)
                if exists != want:
                    of = step.get("on_fail", {})
                    failures.append({
                        "primary": bool(step.get("primary")),
                        "title": step.get("title"),
                        "root": self._fmt(of.get("root", ""), params),
                        "action": [self._fmt(a, params) for a in of.get("action", [])],
                    })

        primary = [f for f in failures if f["primary"]]
        if primary:
            chosen = primary[0]
            secondary = [f for f in failures if f is not chosen]
        elif failures:
            chosen = failures[0]
            secondary = failures[1:]
        else:
            chosen = None
            secondary = []

        if chosen is None:
            verdict = rb.get("default", {"root": "未给出结论", "action": []})
            res["root"] = self._fmt(verdict.get("root", ""), params)
            res["action"] = [self._fmt(a, params) for a in verdict.get("action", [])]
        else:
            res["root"] = chosen["root"]
            res["action"] = chosen["action"]
            res["secondary"] = secondary
        res["verdict"] = "诊断完成"
        return res
