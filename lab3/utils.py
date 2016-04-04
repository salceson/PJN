# coding=utf-8
import codecs
import re
from collections import defaultdict

from metric import levenshtein_metric

__author__ = "Michał Ciołczyk"

REMOVE_NOT_LETTERS = re.compile("[^\w]")


def _file_stats(filename, encoding='utf-8'):
    stats = defaultdict(int)
    with codecs.open(filename, encoding=encoding) as f:
        for line in f:
            for word in line.strip().split():
                word = REMOVE_NOT_LETTERS.sub('', word).lower()
                if word == '':
                    continue
                stats[word] += 1
    return stats


def corpus_stats(filenames, dictionary_len, encondings=defaultdict(lambda: 'utf-8')):
    stats = defaultdict(int)
    for filename in filenames:
        file_stats = _file_stats(filename, encondings[filename])
        stats.update(file_stats)
    stats_sum = float(sum(stats.values())) + dictionary_len
    stats_laplace = defaultdict(lambda: 1. / stats_sum)
    stats_laplace.update({word: (stats[word] + 1.) / stats_sum for word in stats})
    return stats_laplace


def error_stats(filename, enconding='utf-8'):
    distances = defaultdict(int)
    with codecs.open(filename, encoding=enconding) as f:
        for line in f:
            [error, correct] = line.strip().split(';')
            error = REMOVE_NOT_LETTERS.sub('', error).lower()
            correct = REMOVE_NOT_LETTERS.sub('', correct).lower()
            if error == '' or correct == '':
                continue
            distances[levenshtein_metric(error, correct, False)] += 1
    errors_sum = float(sum(distances.values()))
    result = defaultdict(int)
    result.update({dist: dist / errors_sum for dist in distances})
    return result


def get_corrections(filename, enconding='utf-8'):
    with codecs.open(filename, encoding=enconding) as f:
        return list(map(lambda word: REMOVE_NOT_LETTERS.sub('', word.strip().lower()), f.readlines()))
