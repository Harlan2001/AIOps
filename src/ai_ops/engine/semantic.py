# -*- coding: utf-8 -*-
"""本地语义召回（纯标准库，零模型 / 零 API / 零新增依赖）。

两层兜底，仅在 errors.yaml 关键词精确子串未命中时启用：
  1. 同义词子串匹配（synonyms.yaml）：业务口语化说法，确定性、可解释；
  2. 字符 bigram 模糊相似度：处理错别字 / 语序 / 少字多字，阈值保守以防误召回。

设计原则：
- 精确关键词命中永远优先于本模块；
- fuzzy 阈值刻意保守，"尚未配规则"的文本宁可放过也不强行路由（见测试负例）；
- 同义词为数据文件（synonyms.yaml），回流补充无需改代码。
"""
import re

from ai_ops import rules_store

# 去掉参数块 [..] 与占位符 <..>
_BLOCK_RE = re.compile(r"[\[\<][^\[\]\<\>]*[\]\>]")
# 仅保留中文、字母、数字
_KEEP_RE = re.compile(r"[一-鿿a-zA-Z0-9]+")
# 字母数字连续段（作为整体 token，避免被逐字符切碎）
_ALNUM_RE = re.compile(r"[a-zA-Z0-9]{2,}")

# fuzzy 命中阈值（保守）：短语 bigram 被输入覆盖比例 + 对称 Dice
CONT_MIN = 0.72     # 规则短语的 bigram 至少 72% 出现在输入中
DICE_MIN = 0.30     # 同时 Dice 相似度不低于 0.30，防止短词偶然命中
MIN_PHRASE_BIGRAMS = 2
# 编辑距离通道：容忍少量错别字/繁简，4 字词允许 1 字差异(=0.75)；负例实测最高 0.6
EDIT_MIN = 0.75
MIN_EDIT_LEN = 3
MAX_SCAN_LEN = 80   # 输入归一化后超过该长度截断，控制窗口扫描成本


def _load_synonyms():
    """返回 {规则 id: [口语短语...]}，包内基线 + AIOPS_RULES_DIR 外挂覆盖。"""
    return rules_store.load_synonyms()


def normalize(text):
    """清洗为无空白的连续中英数字串：去参数块/占位符/标点，字母转小写。"""
    if not text:
        return ""
    t = _BLOCK_RE.sub(" ", text)
    parts = _KEEP_RE.findall(t)
    return "".join(parts).lower()


def bigrams(s):
    """字符 bigram 集合；字母数字连续段整体作为额外 token；过短串补 unigram。"""
    out = set()
    for i in range(len(s) - 1):
        out.add(s[i:i + 2])
    for m in _ALNUM_RE.findall(s):
        out.add(m)
    if len(s) == 1:
        out.add(s)
    return out


def _dice(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    return 2.0 * inter / (len(a) + len(b))


def _containment(a, b):
    """短语 bigram 集合 b 被输入集合 a 覆盖的比例。"""
    if not b:
        return 0.0
    return len(a & b) / len(b)


def _lev_ratio(a, b):
    """归一化编辑距离相似度（纯标准库 DP），长度差 >2 直接判低，省去无谓计算。"""
    m, n = len(a), len(b)
    if abs(m - n) > 2:
        return 0.0
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        cur = [i]
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost))
        prev = cur
    return 1.0 - prev[n] / max(m, n)


def _best_window_ratio(text, phrase):
    """在输入中扫描与短语长度相近的窗口，取最高编辑相似度（容忍错别字/繁简）。"""
    best = 0.0
    for L in range(max(2, len(phrase) - 1), len(phrase) + 2):
        if L > len(text):
            break
        for i in range(0, len(text) - L + 1):
            r = _lev_ratio(text[i:i + L], phrase)
            if r > best:
                best = r
    return best


class SemanticMatcher:
    """结合 25 类规则做本地语义召回；types 为规则注册表，synonyms 可注入（测试用）。"""

    def __init__(self, types, synonyms=None):
        self.types = types
        synonyms = synonyms if synonyms is not None else _load_synonyms()
        # 每个类型的口语同义词
        self._syn = {t["id"]: synonyms.get(t["id"], []) for t in types}
        # 每个类型用于 fuzzy 的全部短语：title + keywords + 同义词
        self._phrases = {}
        for t in types:
            phrases = [t.get("title", "")] + list(t.get("keywords", [])) \
                + synonyms.get(t["id"], [])
            self._phrases[t["id"]] = [p for p in phrases if p]

    # ---- 同义词子串匹配 ----
    def synonym_match(self, text):
        """返回 (type_cfg, 命中的最长同义词长度)；无命中返回 (None, 0)。"""
        best_t, best_len = None, 0
        for t in self.types:
            hits = [s for s in self._syn.get(t["id"], []) if s in text]
            if not hits:
                continue
            longest = max(len(s) for s in hits)
            # 长度决胜，相同长度保留先定义者（确定性）
            if longest > best_len:
                best_t, best_len = t, longest
        return best_t, best_len

    # ---- 字符 bigram 模糊匹配 ----
    def fuzzy_match(self, text):
        """返回 (type_cfg, score)；无命中返回 (None, 0.0)。

        两个通道任一满足即召回，取最高分：
        - bigram：containment + Dice，处理少字多字/语序；
        - 编辑距离：窗口扫描，处理单字错别字/繁简。
        """
        norm_in = normalize(text)[:MAX_SCAN_LEN]
        a = bigrams(norm_in)
        best_t, best_score = None, 0.0
        for t in self.types:
            for p in self._phrases.get(t["id"], []):
                np = normalize(p)
                # 通道一：字符 bigram
                b = bigrams(np)
                if len(b) >= MIN_PHRASE_BIGRAMS:
                    if _containment(a, b) >= CONT_MIN:
                        dice = _dice(a, b)
                        if dice >= DICE_MIN and dice > best_score:
                            best_t, best_score = t, dice
                # 通道二：编辑距离（短短语错别字/繁简）
                if len(np) >= MIN_EDIT_LEN:
                    er = _best_window_ratio(norm_in, np)
                    if er >= EDIT_MIN and er > best_score:
                        best_t, best_score = t, er
        return best_t, round(best_score, 3)

    def match(self, text):
        """语义召回主入口：先同义词后模糊；返回 (type_cfg, kind, score)。"""
        t, syn_len = self.synonym_match(text)
        if t is not None:
            return t, "synonym", float(syn_len)
        t, score = self.fuzzy_match(text)
        if t is not None:
            return t, "fuzzy", score
        return None, None, 0.0
