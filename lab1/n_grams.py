# coding=utf-8
import re
from collections import Counter

from unidecode import unidecode

__author__ = 'Michał Ciołczyk'

_remove_not_letters = re.compile("[^a-z\s]")


def n_grams_from_data(data, n):
    n_grams = Counter()
    data = unidecode(data.lower()).lower()
    data = _remove_not_letters.sub('', data)
    for word in data.split():
        for n_gram in zip(*(word[c:] for c in range(n))):
            n_grams["".join(n_gram)] += 1
    return n_grams
