# -*- coding: utf-8 -*-
"""训练 ML 前置分流器（两个轻量模型，纯本地 CPU、可离线）。

1) routing   : 文本 → noise / biz / ora / other   一级分流（决定要不要进 LLM）
2) biz_type  : 业务报错文本 → Top30 类型 / other_biz  类型路由

特征：字符级 TF-IDF（中文无需分词，天然吸收措辞/数字/标点变体）
模型：LogisticRegression（线性、可输出概率 → 置信度路由，可解释、毫秒级）
"""
import collections
import csv
import json
import os
import sys
import random

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _ROOT)

from sklearn.model_selection import train_test_split          # noqa: E402
from sklearn.feature_extraction.text import TfidfVectorizer    # noqa: E402
from sklearn.linear_model import LogisticRegression            # noqa: E402
from sklearn.pipeline import Pipeline                          # noqa: E402
from sklearn.metrics import (classification_report, accuracy_score,  # noqa: E402
                             f1_score, confusion_matrix)
import joblib                                                   # noqa: E402

DATA = os.path.join(_ROOT, "data", "ml", "dataset.csv")
MODEL_DIR = os.path.join(_ROOT, "models")
random.seed(42)


def load_rows():
    with open(DATA, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def make_pipeline():
    tf = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4),
                         min_df=2, max_features=60000, sublinear_tf=True)
    lr = LogisticRegression(max_iter=2000, class_weight="balanced", C=10.0)
    return Pipeline([("tfidf", tf), ("lr", lr)])


def downsample(X, y, caps):
    """对训练集多数类做下采样（测试集保持真实分布）。"""
    bucket = collections.defaultdict(list)
    for i, lab in enumerate(y):
        bucket[lab].append(i)
    keep = []
    for lab, idxs in bucket.items():
        random.shuffle(idxs)
        keep += idxs[:caps.get(lab, len(idxs))]
    random.shuffle(keep)
    return [X[i] for i in keep], [y[i] for i in keep]


def fit_and_report(name, X, y, caps=None, test_size=0.2):
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y)
    if caps:
        Xtr, ytr = downsample(Xtr, ytr, caps)
    clf = make_pipeline()
    clf.fit(Xtr, ytr)
    pred = clf.predict(Xte)

    print("=" * 84)
    print("模型：%s" % name)
    print("训练样本 %d，测试样本 %d（测试集保持真实分布）" % (len(ytr), len(yte)))
    print("-" * 84)
    print("准确率 Accuracy : %.4f" % accuracy_score(yte, pred))
    print("宏平均   macro-F1: %.4f" % f1_score(yte, pred, average="macro"))
    print("加权     weighted-F1: %.4f" % f1_score(yte, pred, average="weighted"))
    print("-" * 84)
    print(classification_report(yte, pred, digits=4, zero_division=0))
    labels = sorted(set(yte))
    cm = confusion_matrix(yte, pred, labels=labels)
    print("混淆矩阵（行=真实, 列=预测） 标签顺序：%s" % labels)
    print(cm)
    print("=" * 84)
    return clf, {"labels": labels,
                 "accuracy": round(float(accuracy_score(yte, pred)), 4),
                 "macro_f1": round(float(f1_score(yte, pred, average="macro")), 4),
                 "test_size": len(yte)}


def main():
    rows = load_rows()
    os.makedirs(MODEL_DIR, exist_ok=True)

    # 模型 1：一级分流（noise 下采样到 6000，避免 92.7% 多数类淹没）
    X1 = [r["text"] for r in rows]
    y1 = [r["cls"] for r in rows]
    clf1, m1 = fit_and_report("一级分流器 noise/biz/ora/other",
                              X1, y1, caps={"noise": 6000})
    joblib.dump(clf1, os.path.join(MODEL_DIR, "routing.joblib"))

    # 模型 2：业务类型路由（仅 biz）
    biz = [r for r in rows if r["cls"] == "biz"]
    X2 = [r["text"] for r in biz]
    y2 = [r["biz_type"] for r in biz]
    clf2, m2 = fit_and_report("业务类型路由 Top30 + other_biz", X2, y2)
    joblib.dump(clf2, os.path.join(MODEL_DIR, "biz_type.joblib"))

    meta = {"routing": m1, "biz_type": m2,
            "threshold": 0.8,
            "note": "预测概率最大类 < threshold 视为低置信，升级给 LLM"}
    with open(os.path.join(MODEL_DIR, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print("模型已保存到 %s" % MODEL_DIR)


if __name__ == "__main__":
    main()
