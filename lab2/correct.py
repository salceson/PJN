#!/usr/bin/env python3
# coding=utf-8

import sys

from data_contents import get_data_contents
from metric import levenshtein_metric

__author__ = 'Michał Ciołczyk'

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: %s word_to_correct' % sys.argv[0])
        exit(1)

    word1 = sys.argv[1]
    best_word_dist = 9999999
    best_word = word1

    for word2 in get_data_contents():
        if abs(len(word1) - len(word2)) <= 5:
            dist = levenshtein_metric(word1, word2, False)
            if dist < best_word_dist:
                best_word = word2
                best_word_dist = dist

    print("%s: %s, dist=%f" % (word1, best_word, best_word_dist))
