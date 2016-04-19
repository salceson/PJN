# coding: utf-8
from bisect import bisect
from random import randint

__author__ = "Michał Ciołczyk"


class _MarkovChain(object):
    def __init__(self, ngrams, n, separator):
        self.ngrams = ngrams
        self.n = n
        self.separator = separator

    def generate(self):
        raise NotImplementedError()

    @staticmethod
    def _random_with_probabilities(choices):
        values, weights = zip(*choices.items())
        total = 0
        cumul_weights = []
        for w in weights:
            total += w
            cumul_weights.append(total)
        x = randint(0, total - 1)
        i = bisect(cumul_weights, x)
        return values[i]


class LettersMarkovChain(_MarkovChain):
    def __init__(self, ngrams, n):
        super().__init__(ngrams, n, '')

    def generate(self):
        output = ' ' * (self.n - 1)
        while True:
            last = tuple(output[-self.n + 1:])
            try:
                output += self._random_with_probabilities(self.ngrams[last])
            except ValueError:
                break
        return self.separator.join(output[(self.n - 1):-1])


class WordsMarkovChain(_MarkovChain):
    def __init__(self, ngrams, n):
        super().__init__(ngrams, n, ' ')

    def generate(self):
        output = [''] * self.n
        while True:
            last = tuple(output[-self.n + 1:])
            try:
                output.append(self._random_with_probabilities(self.ngrams[last]))
            except ValueError:
                break
        return self.separator.join(output)
