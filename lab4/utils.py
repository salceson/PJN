# coding: utf-8
from itertools import groupby, combinations
from operator import itemgetter

__author__ = "Michał Ciołczyk"

_CLUSTER_SEPARATOR = '##########\n'


def _read_result(filename):
    clusters = {}
    with open(filename) as f:
        clusters_read = f.read()
        for i, section in enumerate(clusters_read.split(_CLUSTER_SEPARATOR)):
            if not section:
                continue
            for line in section.split('\n'):
                clusters[line] = i
    return clusters


def write_result(result, filename):
    with open(filename, 'w') as f:
        for cluster, lines in groupby(result.items(), itemgetter(1)):
            for line, _ in lines:
                f.write(line + '\n')
            f.write('\n%s' % _CLUSTER_SEPARATOR)


def calculate_quality(result_filename, reference_filename):
    reference = _read_result(reference_filename)
    result = _read_result(result_filename)
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for (a, a_cluster), (b, b_cluster) in combinations(result.items(), 2):
        if reference[a] == reference[b]:
            if a_cluster == b_cluster:
                # True positive - clusters for a and b are the same in BOTH result and reference are the same
                tp += 1
            else:
                # False negative - clusters for a and b are different in result, but NOT in reference
                fn += 1
        else:
            if a_cluster == b_cluster:
                # False positive - clusters for a and b are the same in result, but NOT in reference
                fp += 1
            else:
                # True negative - clusters for a and b are different in both result and reference
                tn += 1
    precision = float(tp) / (tp + fp)
    recall = float(tp) / (tp + fn)
    f1 = 2 * ((precision * recall) / (precision + recall))
    return precision, recall, f1
