# coding=utf-8
import codecs
import re
from collections import defaultdict

from metric import levenshtein_metric

__author__ = "Michał Ciołczyk"

REMOVE_NOT_LETTERS = re.compile("[^\w]")
STOPWORDS_FILE = 'data/stopwords.txt'
STOPWORDS_ENCODING = 'utf-8'


def _file_stats(filename, stopwords, encoding='utf-8'):
    stats = defaultdict(int)
    with codecs.open(filename, encoding=encoding) as f:
        for line in f:
            for word in line.strip().split():
                word = REMOVE_NOT_LETTERS.sub('', word).lower()
                if word == '' or word in stopwords:
                    continue
                stats[word] += 1
    return stats


def corpus_stats(filenames, dictionary_len, stopwords, encodings=defaultdict(lambda: 'utf-8')):
    stats = defaultdict(int)
    for filename in filenames:
        file_stats = _file_stats(filename, stopwords, encodings[filename])
        stats.update(file_stats)
    stats_sum = float(sum(stats.values())) + dictionary_len
    stats_laplace = defaultdict(lambda: 1. / stats_sum)
    stats_laplace.update({word: (stats[word] + 1.) / stats_sum for word in stats})
    return stats_laplace


def error_stats(filename, encoding='utf-8'):
    distances = defaultdict(int)
    with codecs.open(filename, encoding=encoding) as f:
        for line in f:
            [error, correct] = line.strip().split(';')
            error = REMOVE_NOT_LETTERS.sub('', error).lower()
            correct = REMOVE_NOT_LETTERS.sub('', correct).lower()
            if error == '' or correct == '':
                continue
            distances[levenshtein_metric(error, correct, False)] += 1
    errors_sum = float(sum(distances.values()))
    result = defaultdict(int)
    result.update({dist: distances[dist] / errors_sum for dist in distances})
    return result


def get_corrections(filename, stopwords, encoding='utf-8'):
    with codecs.open(filename, encoding=encoding) as f:
        forms = list(map(lambda word: REMOVE_NOT_LETTERS.sub('', word.strip().lower()), f.readlines()))
        return [form for form in forms if form not in stopwords]


def get_stopwords():
    with codecs.open(STOPWORDS_FILE, encoding=STOPWORDS_ENCODING) as f:
        return list(map(lambda x: x.strip(), f.readlines()))
