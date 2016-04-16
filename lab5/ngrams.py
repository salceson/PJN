# coding: utf-8
import codecs
from collections import defaultdict
from math import fsum

__author__ = "Michał Ciołczyk"


class _CorpusStatsAndNGramsStats(object):
    def __init__(self, corpus_filenames, encodings):
        ngrams_stats = defaultdict(int)
        for filename in corpus_filenames:
            with codecs.open(filename, encoding=encodings[filename]) as f:
                file_ngrams = self._get_ngrams_and_stats_from_text(f.read())
                ngrams_stats.update(file_ngrams)
        ngrams_count = fsum(ngrams_stats)
        self.ngrams_stats = {ngram: float(count) / ngrams_count for (ngram, count) in ngrams_stats.values()}

    def _get_ngrams_and_stats_from_text(self, text):
        raise NotImplementedError()


class WordsCorpusStatsAndNGramsStats(_CorpusStatsAndNGramsStats):
    def __init__(self, corpus_filenames, encodings=defaultdict(lambda: 'utf-8')):
        super().__init__(corpus_filenames, encodings)

    def _get_ngrams_and_stats_from_text(self, text):
        first = True
        prev = ''
        ngrams = defaultdict(int)
        for word in text.split(' '):
            if first:
                prev = word
                first = False
                continue
            ngrams[(prev, word)] += 1
            prev = word
        return ngrams


class LettersCorpusStatsAndNGramsStats(_CorpusStatsAndNGramsStats):
    def __init__(self, corpus_filenames, encodings=defaultdict(lambda: 'utf-8')):
        super().__init__(corpus_filenames, encodings)

    def _get_ngrams_and_stats_from_text(self, text):
        ngrams = defaultdict(int)
        for word in text.split(' '):
            prev = ''
            first = True
            for letter in word:
                if first:
                    prev = letter
                    first = False
                    continue
                ngrams[(prev, letter)] += 1
                prev = letter
        return ngrams


class _FileCorpusStatsAndNGramsStats(object):
    def __init__(self, ngrams_stats):
        self.ngrams_stats = ngrams_stats


def read_stats_from_file(filename):
    pass


def write_stats_to_file(stats_object, filename):
    pass
