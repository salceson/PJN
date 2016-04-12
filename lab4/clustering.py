# coding: utf-8
from itertools import combinations

__author__ = "Michał Ciołczyk"

_DEBUG = True
_METRIC_THRESHOLD = 0.333


def cluster(preprocessed_data, metric):
    clusters = {}
    for i, line in enumerate(set(preprocessed_data.values())):
        clusters[line] = i
    for a, b in combinations(sorted(clusters.keys()), 2):
        met = metric(a, b)
        if met <= _METRIC_THRESHOLD:
            if _DEBUG:
                print('\033[1;31m%s\033[0m' % a, '\033[1;32m%s\033[0m' % b)
            clusters[b] = clusters[a]
    return clusters
