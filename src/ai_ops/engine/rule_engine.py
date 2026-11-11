# -*- coding: utf-8 -*-
"""规则引擎（运行时零模型）：正则解析 -> 类型匹配 -> 参数化只读 SQL 诊断树 -> 结构化结论。"""
import re
import warnings
from collections import defaultdict

from ai_ops import rules_store
from ai_ops.engine import parser as P
from ai_ops.engine.db import query

_BIND_RE = re.compile(r"(?<!:):([A-Za-z_]\w*)")


class Engine:
    def __init__(self):
        self.types, self.noise_kw = rules_store.load_registries()
        self._runbooks = {}
        self._warmup()

    def _warmup(self):
        """加载期 fail-fast（阶段 3·②）：预热全部 runbook 并用 977 表清单校验每条 SQL；
        清单缺失时降级 warning（wheel 交付不含 docs/），校验失败时启动即拦截。"""
        from ai_ops.engine import schema_check as SC
        if not SC.catalog_available():
            warnings.warn(
                "表结构清单缺失，跳过规则加载期 fail-fast 校验，运行时降级仍显式可见。")
            return
        errors = []
        for t in self.types:
            rb_name = t.get("runbook")
            if not rb_name:
                continue
            rb = self._load_runbook(rb_name)  # 预热进 _runbooks 缓存
            errors.extend(SC.validate_runbook(rb_name, rb))
        if errors:
            lines = ["规则加载期校验失败（%d 处 SQL 引用与 977 表清单不一致，拒绝启动）："
                     % len(errors)]
            lines += ["  - %s" % e["msg"] for e in errors[:50]]
            if len(errors) > 50:
                lines.append("  ... 其余 %d 处省略" % (len(errors) - 50))
            raise RuntimeError("\n".join(lines))

    def _classify(self, text, errcode):
        """ora / other / biz 判定用解析器通用规则；噪音判定由 noise_rules.yaml 驱动。"""
        if P.is_tech_error(text):
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
        """连接在每次 query 内即开即关，无需常驻连接（保留方法以兼容编排层）。"""
        return

    def _load_runbook(self, name):
        if name not in self._runbooks:
            self._runbooks[name] = rules_store.load_runbook(name)
        return self._runbooks[name]

    def match_type(self, text, errcode):
        """关键词命中为必要条件（错误码在不同业务场景会被复用，不能单独决定类型）；
        错误码仅用于关键词命中后的排序。

        平分规则（B10 修复）：总分相同时，按"命中的最长关键词"长度决胜——完整短语
        （如"自成交预警"）优先于其短子串（如"自成交"），避免子串类型把预警类报错
        误路由到 error 级 runbook；关键词长度仍相同时保留先定义者（确定性）。
        """
        best, best_key = None, None
        for t in self.types:
            matched = [kw for kw in t.get("keywords", []) if kw in text]
            if not matched:
                continue
            kw_hits = len(matched)
            score = kw_hits * 10
            if errcode and errcode in t.get("err_codes", []):
                score += 2
            longest = max(len(k) for k in matched)
            # 比较键：总分 → 命中关键词最长长度（越长越具体）
            key = (score, longest)
            if best_key is None or key > best_key:
                best, best_key = t, key
        return best, (best_key[0] if best_key else 0)

    def _build_params(self, raw, ldate, type_cfg, rb, base=None):
        # 基础：错误记录自带的业务字段（member/client/contract/trader...）
        params = {k: v for k, v in (base or {}).items()
                  if v not in (None, "")}
        # 报错文本里显式写出的 [字段=>值] 覆盖（param_alias 归一化）
        alias = type_cfg.get("param_alias", {})
        for cn, val in P.extract_params(raw).items():
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
        # 参数值映射（报错文本中文 -> 库内码值，如 市场:现货->0）
        for name, vmap in (rb.get("param_value_maps") or {}).items():
            if params.get(name) in vmap:
                params[name] = vmap[params[name]]
        return params

    def _run_sql(self, sql, params):
        need = set(_BIND_RE.findall(sql))
        present = {k for k, v in params.items() if v not in (None, "")}
        missing = need - present
        if missing:
            return {"status": "missing_params", "missing": sorted(missing)}
        b = {k: params[k] for k in need}
        try:
            cols, rows = query(sql, b)
        except Exception as e:
            # 表/列缺失、连接失败等：诊断降级为 error，不让单条失败拖垮整条诊断
            return {"status": "error", "error": str(e)[:200]}
        return {"status": "ok", "cols": cols, "rows": [list(r) for r in rows]}

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
            res["verdict"] = "数据库技术错误（SQLSTATE/基础设施，本期不诊断，建议转 DBA/运维）"
            return res
        if res["class"] == "other":
            # 报警/提示类文本（不含"失败/异常/错误"等词）也会归入 other，
            # 仍尝试类型匹配，匹配不上再走兜底，让报警通用模板有机会命中。
            tcfg, score = self.match_type(text, errcode)
            if not tcfg:
                res["verdict"] = "未识别类型，进入通用兜底 / 回流待补规则"
                return res
        else:
            tcfg, score = self.match_type(text, errcode)
            if not tcfg:
                res["verdict"] = "业务报错但未匹配规则，进入兜底 / 回流待补规则"
                return res

        rb = self._load_runbook(tcfg["runbook"])
        params = self._build_params(text, ldate, tcfg, rb, base=record.get("params"))
        res.update({"type": tcfg, "runbook": rb["id"], "params": params, "evidence": []})

        # 跑完所有检查，收集全部失败项，再按"主检查优先"综合判定
        failures = []
        sql_errors = []
        missing_params = []
        for step in rb["steps"]:
            r = self._run_sql(step["sql"], params)
            ev = {"id": step["id"], "title": step.get("title"), "kind": step["type"],
                  "primary": bool(step.get("primary")), "r": r}
            res["evidence"].append(ev)
            if step["type"] == "sql_check":
                if r["status"] == "ok":
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
                elif r["status"] == "error":
                    sql_errors.append({"step": step.get("id"), "error": r.get("error", "")})
                elif r["status"] == "missing_params":
                    # B4：缺参不再静默跳过，显式写入结构化结果，API/报告/调用方可感知
                    missing_params.append(
                        {"step": step.get("id"), "missing": r.get("missing", [])})
        if sql_errors:
            res["sql_errors"] = sql_errors
        if missing_params:
            res["missing_params"] = missing_params

        # B8：证据可信度标记——主检查是否有成功取证、全部检查是否完整
        check_evs = [ev for ev in res["evidence"] if ev["kind"] == "sql_check"]
        primary_evs = [ev for ev in check_evs if ev["primary"]]
        # 有 primary 标记时以 primary 为准；无 primary 的 runbook 退化为任一 sql_check
        watch = primary_evs if primary_evs else check_evs
        primary_ok = any(ev["r"]["status"] == "ok" for ev in watch)
        evidence_complete = bool(check_evs) and all(
            ev["r"]["status"] == "ok" for ev in check_evs)
        res["primary_evidence_ok"] = primary_ok
        res["evidence_complete"] = evidence_complete

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
