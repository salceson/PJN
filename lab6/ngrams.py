# coding: utf-8
import codecs
import re
from collections import Counter

__author__ = "Michał Ciołczyk"

_NOT_LETTERS_PATTERN = re.compile('[\W\d]+', re.UNICODE)
_2GRAMS_FILENAME = 'out/2grams.csv'
_3GRAMS_FILENAME = 'out/3grams.csv'


def _n_grams_from_data(data, n):
    n_grams = Counter()
    for n_gram in zip(*(data[c:] for c in range(n))):
        n_grams[" ".join(n_gram).lower()] += 1
    return n_grams


def n_grams_stats(filename, encoding='utf-8'):
    print("Reading file %s..." % filename)
    with codecs.open(filename, encoding=encoding) as f:
        data = f.read().strip()
        data = _NOT_LETTERS_PATTERN.sub(' ', data)
        data = data.split()
        print("\tDone")
        print("Generating 2grams stats...")
        with codecs.open(_2GRAMS_FILENAME, 'w', 'utf-8') as f2:
            for gram, count in _n_grams_from_data(data, 2).items():
                f2.write('%s,%d\n' % (gram, count))
        print("\tDone")
        print("Generating 3grams stats...")
        with codecs.open(_3GRAMS_FILENAME, 'w', 'utf-8') as f3:
            for gram, count in _n_grams_from_data(data, 3).items():
                f3.write('%s,%d\n' % (gram, count))
        print("\tDone")
