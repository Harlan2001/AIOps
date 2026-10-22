# -*- coding: utf-8 -*-
"""报错文本解析（纯规则，零模型）。

能力：
- 噪音 / 技术错误(ORA) / 业务报错 / 其他 分类
- 报错文本归一化"骨架"（用于聚类与文本兜底匹配）
- 从一条具体报错抽取 [字段=>值] / [字段->值] 参数
- 解析 LSECTION 调用链，定位 PKC 包 / SP 过程 / 行号
- 业务报错粗分类
"""
import re

# [字段=>值] 或 [字段->值]
_PARAM_RE = re.compile(r"\[([^\[\]=>\-]+?)\s*(=>|->)\s*([^\]]*)\]")
_NUM_RE = re.compile(r"\d+")
_WS_RE = re.compile(r"\s+")
# CLEAR.PKC_MAIN.SP_XXX:940  或  block:2.CLEAR.PKC_..SP_..:940
_CHAIN_RE = re.compile(r"(?:[A-Z]+\.)?(PKC_[A-Z_]+)\.(SP_[A-Z_]+):(\d+)")
_PKG_RE = re.compile(r"PKC_[A-Z_]+")
_CN_RE = re.compile(r"[\u4e00-\u9fff]")

# 定时任务流水类"假 ERROR"（成功/无数据/完成）
NOISE_KW = ("成功", "完成", "启动", "恢复", "无需要发送", "已处理", "已恢复")
# 真正的业务报错词
ERROR_KW = ("不存在", "失败", "异常", "错误", "不允许", "不可", "不足", "不能为空", "不能",
            "冲突", "超时", "重复", "非法", "无法", "请检查", "未", "没有", "不一致", "不匹配")


def is_chinese(text):
    return bool(_CN_RE.search(text or ""))


def is_ora(text):
    t = text or ""
    return ("ORA-" in t) or ("SQLCODE" in t)


def normalize_skeleton(text):
    """把 [字段=>值] 参数值占位为 ?，数字→#，得到聚类骨架。"""
    if not text:
        return ""
    t = _PARAM_RE.sub(lambda m: "[" + m.group(1).strip() + m.group(2) + "?]", text)
    t = _NUM_RE.sub("#", t)
    t = _WS_RE.sub(" ", t).strip()
    return t[:120]


def extract_params(text):
    """从一条具体报错抽取参数：返回 {字段名: 值}。"""
    d = {}
    for field, _sep, val in _PARAM_RE.findall(text or ""):
        field = field.strip()
        if field not in d:
            d[field] = val.strip()
    m = re.search(r"尚缺\s*<\s*([0-9]+)\s*>", text or "")
    if m:
        d["尚缺"] = m.group(1)
    return d


def parse_lsection(lsection):
    """解析调用链：返回顶层/最深包、过程、行号、模块标签。"""
    if not lsection:
        return {}
    chain = _CHAIN_RE.findall(lsection)
    pkgs = _PKG_RE.findall(lsection)
    res = {"pkgs": sorted(set(pkgs))}
    if chain:
        top_pkg, top_proc, _ = chain[0]
        deep_pkg, deep_proc, deep_line = chain[-1]
        res.update({
            "top_pkg": top_pkg,
            "top_proc": top_proc,
            "deep_pkg": deep_pkg,
            "deep_proc": deep_proc,
            "deep_line": deep_line,
            "module_label": deep_pkg,
        })
    elif pkgs:
        res["module_label"] = pkgs[-1]
    return res


def classify(text, errcode=0):
    """返回 noise / ora / biz / other。"""
    t = text or ""
    if is_ora(t):
        return "ora"
    if not is_chinese(t):
        return "other"
    if any(k in t for k in ERROR_KW):
        return "biz"
    if errcode and errcode != 0:
        return "biz"
    if any(k in t for k in NOISE_KW):
        return "noise"
    return "other"


def coarse_category(text):
    """业务报错粗分类（种子用，后续由专家/LLM 精修）。"""
    t = text or ""
    if any(k in t for k in ("未复核", "未提交", "未完全分配", "未完成", "未录入", "正在发送中")):
        return "流程未就绪"
    if any(k in t for k in ("不存在", "未设置", "未找到", "没有", "缺失", "无数据")):
        return "数据缺失"
    if any(k in t for k in ("不足", "不允许", "不能", "异常", "不一致", "不匹配")):
        return "业务规则校验"
    if any(k in t for k in ("不能为空", "请重新输入")):
        return "录入校验"
    if any(k in t for k in ("密码", "IP", "登录", "注册", "安全标识", "用户名")):
        return "权限登录"
    if "失败" in t:
        return "操作失败"
    return "待分类"
