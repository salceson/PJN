#!/usr/bin/env python3
# coding=utf-8

__author__ = 'Michał Ciołczyk'

DELETE_COST = 1
INSERT_COST = 1
CHANGE_COST = 1
CZECH_ERROR_COST = 0.5
DIACRITIC_ERROR_COST = 0.25
SPELLING_ERROR_COST = 0.5

COSTS_OF_MISTAKES = {
    'ą': [
        ('a', DIACRITIC_ERROR_COST),  # cost of a <-> ą is DIACRITIC_ERROR_COST
        ('on', SPELLING_ERROR_COST - CHANGE_COST)  # cost of a <-> on is SPELLING_ERROR_COST,
        #                                            but on the 'n' letter it will find it one more time
        #                                            - so we need to subtract
    ],
    'ć': [
        ('c', DIACRITIC_ERROR_COST)
    ],
    'ę': [
        ('e', DIACRITIC_ERROR_COST),
        ('en', SPELLING_ERROR_COST - CHANGE_COST)
    ],
    'ł': [
        ('l', DIACRITIC_ERROR_COST)
    ],
    'ń': [
        ('n', DIACRITIC_ERROR_COST)
    ],
    'ó': [
        ('o', DIACRITIC_ERROR_COST)
    ],
    'ś': [
        ('s', DIACRITIC_ERROR_COST),
        ('si', SPELLING_ERROR_COST - CHANGE_COST)
    ],
    'ż': [
        ('z', DIACRITIC_ERROR_COST),
        ('rz', SPELLING_ERROR_COST - CHANGE_COST)
    ],
    'ź': [
        ('z', DIACRITIC_ERROR_COST)
    ],
    'h': [
        ('ch', SPELLING_ERROR_COST - CHANGE_COST)
    ],
    'u': [
        ('ó', SPELLING_ERROR_COST)
    ],
    'c': [
        ('dz', SPELLING_ERROR_COST - CHANGE_COST)
    ],
    'łu': [
        ('u', SPELLING_ERROR_COST - CHANGE_COST)
    ],
    'trz': [
        ('cz', SPELLING_ERROR_COST - 2 * CHANGE_COST),
        ('tsz', SPELLING_ERROR_COST - CHANGE_COST)
    ],
    'wsz': [
        ('fsz', SPELLING_ERROR_COST - CHANGE_COST)
    ],
}


# noinspection PyTypeChecker
def levenshtein_metric(word1, word2, basic_metric=True, best_metric=99999999):
    lev = [[max(i, j) if min(i, j) == 0 else 0 for j in range(len(word2) + 1)] for i in range(len(word1) + 1)]
    costs = [[CHANGE_COST for _ in range(len(word2) + 1)] for __ in range(len(word1) + 1)]

    for i in range(1, len(word1) + 1):
        for j in range(1, len(word2) + 1):
            if not basic_metric:
                # here we operate on word which indices are [0, n-1], but loops are [1, n] - so some magic
                i -= 1
                j -= 1
                if word1[i] == word2[j] and costs[i][j] == CHANGE_COST:
                    costs[i][j] = 0
                if i > 1 and j > 1 and word1[i - 1] == word2[j] and word2[j - 1] == word1[i]:
                    costs[i - 1][j - 1] = CHANGE_COST
                    costs[i][j] = CZECH_ERROR_COST - CHANGE_COST
                else:
                    check1 = word1[i:]
                    check2 = word2[j:]
                    for token, possible_mistakes in COSTS_OF_MISTAKES.items():
                        if check1.startswith(token):
                            for mistake_token, mistake_cost in possible_mistakes:
                                if check2.startswith(mistake_token):
                                    current_cost = costs[i + len(token) - 1][j + len(mistake_token) - 1]
                                    costs[i + len(token) - 1][j + len(mistake_token) - 1] = min(mistake_cost,
                                                                                                current_cost)

                        if check2.startswith(token):
                            for mistake_token, mistake_cost in possible_mistakes:
                                if check1.startswith(mistake_token):
                                    current_cost = costs[i + len(mistake_token) - 1][j + len(token) - 1]
                                    costs[i + len(mistake_token) - 1][j + len(token) - 1] = min(mistake_cost,
                                                                                                current_cost)
                i += 1
                j += 1

            are_same = 0 if word1[i - 1] == word2[j - 1] else 1
            dist = min(lev[i - 1][j] + DELETE_COST,
                       lev[i][j - 1] + INSERT_COST,
                       lev[i - 1][j - 1] + are_same * costs[i - 1][j - 1])
            lev[i][j] = dist
            if abs(i - j) <= abs(len(word1) - len(word2)) and dist > best_metric:
                return dist

    return lev[len(word1)][len(word2)]


if __name__ == "__main__":
    print(levenshtein_metric("biurko", "pióro"))
    print(levenshtein_metric("biurko", "biurko"))
    print(levenshtein_metric("biurko", "biukro"))
    print(levenshtein_metric("biurko", "biórko"))
    print(levenshtein_metric("testując", "testujac"))
    print(levenshtein_metric("biurko", "biukro"))
    print("---")
    print(levenshtein_metric("biurko", "pióro", False))
    print(levenshtein_metric("biurko", "biurko", False))
    print(levenshtein_metric("biurko", "biukro", False))
    print(levenshtein_metric("biurko", "biukro", False))
    print(levenshtein_metric("biurko", "biórko", False))
    print(levenshtein_metric("testując", "testujac", False))
