# coding: utf-8
import codecs
import re
from collections import Counter

from flection import basic_form

__author__ = "Michał Ciołczyk"

_NOT_LETTERS_PATTERN = re.compile('[\W\d]+', re.UNICODE)


def read_data_file(filename, encoding='utf-8'):
    with codecs.open(filename, encoding=encoding) as f:
        return _NOT_LETTERS_PATTERN.sub(' ', f.read().strip()).split()


def stats(filename, encoding='utf-8'):
    corpus = read_data_file(filename, encoding)
    corpus_len = len(corpus)
    stats = Counter()
    for word in corpus:
        word = str(word.strip().lower())
        word_basic_form = basic_form(word)
        if not word_basic_form:
            continue
        stats[word_basic_form] += 1
    return stats, corpus_len
