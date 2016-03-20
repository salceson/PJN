#!/usr/bin/env python3
# coding=utf-8

__author__ = 'Michał Ciołczyk'

DELETE_COST = 1
INSERT_COST = 1
CHANGE_COST = 1
CZECH_ERROR_COST = 0.5


# noinspection PyTypeChecker
def levenshtein_metric(word1, word2, basic_metric=True):
    lev = [[max(i, j) if min(i, j) == 0 else 0 for j in range(len(word2) + 1)] for i in range(len(word1) + 1)]

    for i in range(1, len(word1) + 1):
        for j in range(1, len(word2) + 1):
            aiaj1 = 0 if word1[i - 1] == word2[j - 1] else 1
            # Idea taken from: https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
            if i > 1 and j > 1 and word1[i - 2] == word2[j - 1] and word1[i - 1] == word2[j - 2] and not basic_metric:
                lev[i][j] = min(lev[i - 1][j] + DELETE_COST, lev[i][j - 1] + INSERT_COST,
                                lev[i - 1][j - 1] + aiaj1 * CHANGE_COST,
                                lev[i - 2][j - 2] + CHANGE_COST + CZECH_ERROR_COST)
            else:
                lev[i][j] = min(lev[i - 1][j] + DELETE_COST, lev[i][j - 1] + INSERT_COST,
                                lev[i - 1][j - 1] + aiaj1 * CHANGE_COST)
    return lev[len(word1)][len(word2)]


if __name__ == "__main__":
    print(levenshtein_metric("biurko", "pióro"))
    print(levenshtein_metric("biurko", "biurko"))
    print(levenshtein_metric("biurko", "biukro"))
    print(levenshtein_metric("biurko", "biukro", False))
