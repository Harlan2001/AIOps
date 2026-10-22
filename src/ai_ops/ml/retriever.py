# -*- coding: utf-8 -*-
"""ML 相似案例召回（运维版 RAG 的检索层）。

对全部历史业务报错建字符级 TF-IDF 索引，输入一条新报错，
用余弦相似度召回最相似的历史案例（按骨架聚合），作为 LLM 的证据，
解决"LLM 上下文装不下、无法在海量日志里找相关历史"的问题。
"""
import collections
import csv

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from ai_ops import paths


class SimilarCaseIndex:
    def __init__(self, records):
        self.records = records
        self.texts = [r["text"] for r in records]
        if records:
            self.vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4),
                                       min_df=1, sublinear_tf=True)
            self.matrix = self.vec.fit_transform(self.texts)
        else:
            # 数据集缺失时静默降级：无历史案例可召回（不阻断主流程）
            self.vec = None
            self.matrix = None

        # 预聚合：骨架 -> 统计信息
        self.groups = {}
        for idx, r in enumerate(records):
            sk = r["skeleton"]
            g = self.groups.setdefault(sk, {
                "skeleton": sk, "count": 0, "last_date": "",
                "errcodes": collections.Counter(), "modules": collections.Counter(),
                "biz_type": r.get("biz_type", ""), "sample": r["text"]})
            g["count"] += 1
            if r["ldate"] > g["last_date"]:
                g["last_date"] = r["ldate"]
                g["sample"] = r["text"]
            if r.get("errcode"):
                g["errcodes"][str(r["errcode"])] += 1
            if r.get("module"):
                g["modules"][r["module"]] += 1

    @classmethod
    def from_dataset(cls, path=None):
        path = path or paths.dataset_csv()
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                records = [r for r in csv.DictReader(f) if r["cls"] == "biz"]
        except FileNotFoundError:
            print("[召回] 数据集不存在（%s），相似案例召回降级为空" % path)
            records = []
        return cls(records)

    def query(self, text, top_k=5):
        if not self.records:
            return []
        q = self.vec.transform([text])
        scores = linear_kernel(q, self.matrix).ravel()
        # 每个骨架只保留其最高实例分，按骨架去重排序
        best = {}
        order = scores.argsort()[::-1]
        for idx in order:
            sk = self.records[idx]["skeleton"]
            if sk not in best:
                best[sk] = float(scores[idx])
            if len(best) >= top_k * 4 and scores[idx] <= 0:
                break
            if len(best) >= top_k * 6:
                break
        ranked = sorted(best.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
        out = []
        for sk, score in ranked:
            g = self.groups[sk]
            out.append({
                "similarity": round(score, 3),
                "skeleton": sk,
                "biz_type": g["biz_type"],
                "count": g["count"],
                "last_date": g["last_date"][:10],
                "errcodes": [c for c, _ in g["errcodes"].most_common(3)],
                "modules": [m for m, _ in g["modules"].most_common(2)],
                "sample": g["sample"][:160],
            })
        return out


if __name__ == "__main__":
    idx = SimilarCaseIndex.from_dataset()
    for t in ["[合约=>Au9999]结算价不存在",
              "[交易员=>xx]持仓不足,尚缺<2>",
              "登录的时候提示用户名密码不对"]:
        print("=" * 80)
        print("查询：", t)
        for hit in idx.query(t, top_k=3):
            print("  %.3f | %d次 | %s | %s" %
                  (hit["similarity"], hit["count"], hit["errcodes"], hit["skeleton"][:60]))
