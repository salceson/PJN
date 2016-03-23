#!/usr/bin/env python3
# coding=utf-8

import sys
from time import time

from data_contents import get_data_contents
from metric import levenshtein_metric

__author__ = 'Michał Ciołczyk'

MAX_LENGTH_DIFFERENCE = 3

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: %s word_to_correct' % sys.argv[0])
        exit(1)

    word1 = sys.argv[1]
    best_word_dist = 9999999
    best_word_fits = [word1]

    time1 = time()
    dictionary = get_data_contents()
    if not (word1 in dictionary):
        for word2 in dictionary:
            if abs(len(word1) - len(word2)) <= MAX_LENGTH_DIFFERENCE:
                dist = levenshtein_metric(word1, word2, False, best_word_dist)
                if dist < best_word_dist:
                    best_word_fits = [word2]
                    best_word_dist = dist
                elif dist == best_word_dist:
                    best_word_fits.append(word2)
    else:
        best_word_dist = 0
    time2 = time()

    print("%s: %s, dist=%f" % (word1, best_word_fits, best_word_dist))
    print("Run for %f seconds." % (time2 - time1))
