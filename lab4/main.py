# coding: utf-8
import sys
from time import time

from clustering import cluster
from metrics import dice_metric, cosine_metric, lcs_metric
from preprocessing import process
from utils import write_result, calculate_quality

__author__ = "Michał Ciołczyk"

_ACTIONS = ["compare", "dice", "cosine", "lcs"]
_METRICS = ["dice", "cosine", "lcs"]
_INPUT_FILENAME = "data/lines.txt"
_OUTPUT_PATTERN = "data/output_%s.txt"
_REFERENCE_FILENAME = "data/clusters.txt"
_DEBUG = False
_THRESHOLDS = {
    'dice': 0.12,
    'cosine': 0.75,
    'lcs': 0.333
}


def _usage():
    print("Usage: python %s <operation>" % args[0])
    print("\tOperation one of: %s" % _ACTIONS)
    exit(1)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        _usage()
    action = args[1]
    if action not in _ACTIONS:
        _usage()
    time1 = time()
    if action == "compare":
        print("Calculating statistics...")
        for metric in _METRICS:
            try:
                precision, recall, f1 = calculate_quality(_OUTPUT_PATTERN % metric, _REFERENCE_FILENAME)
                print("Metric %s:" % metric)
                print("\tPrecision: %f, recall: %f, f1: %f" % (precision, recall, f1))
            except:
                pass
        time2 = time()
        print("Run for %f s." % (time2 - time1))
    else:
        metric_txt = action
        metric = dice_metric if action == 'dice' else cosine_metric if action == 'cosine' else lcs_metric
        print("Preprocessing data...")
        print("Input: %s" % _INPUT_FILENAME)
        counter = 0
        preprocessed = {}
        result = {}
        with open(_INPUT_FILENAME) as input:
            for line in input:
                preprocessed_line = process(line)
                preprocessed[line] = preprocessed_line
                if _DEBUG and counter % 50 == 0:
                    print("%s => %s" % (line, preprocessed_line))
                counter += 1
        print("Clustering...")
        clusters = cluster(preprocessed, metric, _THRESHOLDS[metric_txt], _DEBUG)
        for line, preprocessed_line in preprocessed.items():
            result[line] = clusters[preprocessed_line]
        print("Writing result...")
        write_result(result, _OUTPUT_PATTERN % metric_txt)
        time2 = time()
        print("Run for %f s." % (time2 - time1))
