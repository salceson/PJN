#!/usr/bin/env python3
# coding=utf-8

__author__ = 'Michał Ciołczyk'


def levenshtein_metric(word1, word2):
    lev = [[max(i, j) if min(i, j) == 0 else 0 for j in range(len(word2) + 1)] for i in range(len(word1) + 1)]

    for i in range(1, len(word1) + 1):
        for j in range(1, len(word2) + 1):
            aiaj1 = 0 if word1[i - 1] == word2[j - 1] else 1
            lev[i][j] = min(lev[i - 1][j] + 1, lev[i][j - 1] + 1, lev[i - 1][j - 1] + aiaj1)
    return lev[len(word1)][len(word2)]


if __name__ == "__main__":
    print(levenshtein_metric("biurko", "pióro"))
    print(levenshtein_metric("biurko", "biurko"))
