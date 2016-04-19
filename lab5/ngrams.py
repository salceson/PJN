# coding: utf-8
import codecs
import pickle
import re
from collections import defaultdict, Counter

__author__ = "Michał Ciołczyk"

_TEXT_SEPARATOR = re.compile('\n#[0-9]{6}\n')
_NOT_LETTERS = re.compile('[^a-ząćęłóńśżź]+')


class _NGramsStats(object):
    def __init__(self, n, corpus_filename, encoding='utf-8'):
        self.n = n
        self.ngrams_stats = defaultdict(Counter)
        with codecs.open(corpus_filename, encoding=encoding) as f:
            texts = f.read()
            texts = re.split(_TEXT_SEPARATOR, texts)
            for input in self._generate_texts_from_raw_input(texts):
                for it in zip(*(input[k:] for k in range(self.n))):
                    self.ngrams_stats[it[:self.n - 1]][it[self.n - 1]] += 1

    def _generate_texts_from_raw_input(self, input):
        raise NotImplementedError()


class WordsNGramsStats(_NGramsStats):
    def __init__(self, n, corpus_filename, encoding='utf-8'):
        super().__init__(n, corpus_filename, encoding)

    def _generate_texts_from_raw_input(self, input):
        return [[''] * self.n + re.split('\s+', text.strip()) for text in input if text]


class LettersNGramsStats(_NGramsStats):
    def __init__(self, n, corpus_filename, encoding='utf-8'):
        super().__init__(n, corpus_filename, encoding)

    # noinspection PyTypeChecker
    def _generate_texts_from_raw_input(self, input):
        texts = [_NOT_LETTERS.sub(' ', text.strip()) for text in input if text]
        return [' ' * (self.n - 1) + word + '^' for text in texts for word in text.split()]


def read_stats_from_file(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def write_stats_to_file(stats_object, filename):
    with open(filename, 'wb') as f:
        pickle.dump(stats_object.ngrams_stats, f)
