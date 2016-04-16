# coding: utf-8
from math import fsum
from operator import itemgetter
from random import random, shuffle

__author__ = "Michał Ciołczyk"


class MarkovChain(object):
    def __init__(self, corpus_ngrams_stats, separator=''):
        self.separator = separator
        self.transitions = {}
        for (state, _) in corpus_ngrams_stats.keys():
            self.transitions[state] = []
        for (prev_state, next_state), prob in corpus_ngrams_stats.items():
            self.transitions[prev_state].append((next_state, prob))
        for state in self.transitions:
            if not self.transitions[state]:
                self.transitions[state].append((state, 1.0))
            else:
                prob_sum = fsum(self.transitions[state])
                self.transitions[state] = [(state, prob / prob_sum) for (state, prob) in self.transitions[state]]
        for state in self.transitions:
            self.transitions[state] = sorted(self.transitions[state], key=itemgetter(1), reverse=True)

    def generate(self, n):
        output = []
        state = shuffle(list(self.transitions.keys()))[0]
        output.append(state)
        for i in range(n-1):
            state = self._random_with_probabilities(self.transitions[state])
            output.append(state)
        return self.separator.join(output)

    @staticmethod
    def _random_with_probabilities(items_with_sorted_probabilities):
        rand_num = random()
        prob_sum = 0.0
        for (item, prob) in items_with_sorted_probabilities:
            if rand_num < (prob + prob_sum):
                return item
            prob_sum += prob
