# coding: utf-8
import re
from collections import Counter
from math import fsum

from unidecode import unidecode

__author__ = "Michał Ciołczyk"

_REMOVE_NOT_LETTERS = re.compile("[^a-z\s]")
_N = 2


def _normalize(vec):
    vec_sum = fsum(vec.values())
    normalized = {k: v / vec_sum for k, v in vec.items()}
    return normalized


def _n_grams_from_data(data, n=_N):
    n_grams = Counter()
    data = unidecode(data.lower()).lower()
    data = _REMOVE_NOT_LETTERS.sub('', data)
    for word in data.split():
        for n_gram in zip(*(word[c:] for c in range(n))):
            n_grams["".join(n_gram)] += 1
    return n_grams


# noinspection PyTypeChecker
def dice_metric(line1, line2):
    ngrams1 = _n_grams_from_data(line1)
    ngrams2 = _n_grams_from_data(line2)
    intersection = set(ngrams1.keys()) & set(ngrams2.keys())
    try:
        return 1.0 - 2 * len(intersection) / (len(ngrams1.keys()) + len(ngrams2.keys()))
    except ZeroDivisionError:
        return 1.0


def cosine_metric(line1, line2):
    try:
        ngrams1 = _normalize(_n_grams_from_data(line1))
        ngrams2 = _normalize(_n_grams_from_data(line2))
        intersection = set(ngrams1.keys()) & set(ngrams2.keys())
        inner_product = fsum([ngrams1.get(key, 0) * ngrams2.get(key, 0) for key in intersection])
        return 1.0 - inner_product
    except ZeroDivisionError:
        return 1.0


def lcs_metric(line1, line2):
    len_a = len(line1)
    len_b = len(line2)
    C = [[0] * (len_b + 1) for _ in range(len_a + 1)]
    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            C[i][j] = C[i - 1][j - 1] + 1 if line1[i - 1] == line2[j - 1] else max(C[i][j - 1], C[i - 1][j])
    try:
        return 1.0 - C[len_a][len_b] * 1.0 / max(len_a, len_b)
    except ZeroDivisionError:
        return 1.0
