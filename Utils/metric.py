import pickle as pickle
import os
import pandas as pd
import sklearn
import numpy as np
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score


def klue_re_micro_f1(preds, labels):
    """KLUE-RE micro f1 (except no_relation)"""
    label_list = [
        "관계_없음",
        "인물:참가",
        "인물:소속",
        "인물:결과",
        "단체:결과",
        "단체:참가",
        "행사:장소",
        "행사:일시",
        "행사:하위_행사"
    ]
    no_relation_label_idx = label_list.index("관계_없음")
    label_indices = list(range(len(label_list)))
    label_indices.remove(no_relation_label_idx)
    return sklearn.metrics.f1_score(labels, preds, average="micro", labels=label_indices) * 100.0


def klue_re_auprc(probs, labels):
    """KLUE-RE AUPRC (with no_relation)"""
    labels = np.eye(9)[labels]  # 원핫 인코딩 해주는 부분

    score = np.zeros((9,))
    for c in range(9):  # c는 각 클래스
        # c에 대한 정답 레이블 확인 (열 요소 추출)
        targets_c = labels.take([c], axis=1).ravel()
        if targets_c.sum() == 0:  # 해당하는 클래스가 하나도 없다면 skip
            continue
        # c에 대한 확률(만약 logit이라면?) 레이블 확인 (열 요소 추출)
        preds_c = probs.take([c], axis=1).ravel()
        precision, recall, _ = sklearn.metrics.precision_recall_curve(
            targets_c, preds_c)  # 세번째 반환 값이 바로 임계값, logit의 범위에 따라 자동으로 반환해주는 듯
        score[c] = sklearn.metrics.auc(recall, precision)
    return np.average(score) * 100.0
