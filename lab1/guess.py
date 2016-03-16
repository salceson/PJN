# coding=utf-8
import sys
from collections import Counter
from math import sqrt, fsum
from pprint import pprint

from n_grams import n_grams_from_data

__author__ = 'Michał Ciołczyk'


def len_vec(vec):
    return sqrt(fsum(v ** 2 for v in vec.values()))


def normalize(vec):
    s = fsum(vec.values())
    normalized_v0 = {k: v / s for k, v in vec.items()}
    return normalized_v0


# All metrics expect normalized vectors below

def euclidean_metric(stat1, stat2):
    keys = set(stat1.keys()) | set(stat2.keys())
    sum = 0
    for key in keys:
        sum += (stat1.get(key, 0) - stat2.get(key, 0)) ** 2
    return sqrt(sum)


def taxi_metric(stat1, stat2):
    keys = set(stat1.keys()) | set(stat2.keys())
    sum = 0
    for key in keys:
        sum += abs(stat1.get(key, 0) - stat2.get(key, 0))
    return sum


def max_metric(stat1, stat2):
    keys = set(stat1.keys()) | set(stat2.keys())
    sum = 0
    for key in keys:
        sum = max(sum, abs(stat1.get(key, 0) - stat2.get(key, 0)))
    return sum


def cosine_metric(stat1, stat2):
    keys = set(stat1.keys()) | set(stat2.keys())
    sum = 0
    for key in keys:
        sum += stat1.get(key, 0) * stat2.get(key, 0)
    return 1 - sum


if __name__ == "__main__":
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("Usage: %s input_file metric n [show]" % sys.argv[0])
        exit(1)

    input_file = sys.argv[1]
    metric = sys.argv[2]
    n = int(sys.argv[3])
    show = len(sys.argv) == 5

    languages = ["en", "es", "fi", "de", "pl", "it"]

    best = 100000000
    best_lng = "nope"

    data = ""

    with open(input_file) as f:
        data = f.read().lower()

    n_gram_from_text = n_grams_from_data(data, n)
    input_stat = normalize(n_gram_from_text)
    distances = {}

    for lang in languages:
        lang_stat = Counter()
        with open("out/lang_%s_%d.txt" % (lang, n)) as f:
            for line in f:
                key, count = line.split(' ')
                count = int(count)
                lang_stat[key] += count
        lang_stat = normalize(lang_stat)

        dist = 20000000000

        if metric == 'euclidean':
            dist = euclidean_metric(lang_stat, input_stat)
        if metric == 'cosine':
            dist = cosine_metric(lang_stat, input_stat)
        if metric == 'max':
            dist = max_metric(lang_stat, input_stat)
        if metric == 'taxi':
            dist = taxi_metric(lang_stat, input_stat)

        distances[lang] = dist

        if dist < best:
            best = dist
            best_lng = lang

    print(best_lng)
    if show:
        pprint(distances)
