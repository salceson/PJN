# coding: utf-8
from collections import Counter, defaultdict
from clp import GrammarCase

__author__ = "Michał Ciołczyk"


def prepositions_map_to_stats(prepositions_map):
    prepositions_stats = defaultdict(Counter)
    samples = defaultdict(lambda: defaultdict(list))
    for preposition, nouns in prepositions_map.items():
        for noun_orig, noun_clp in nouns:
            grammar_cases = noun_clp.grammar_case(noun_orig)
            if preposition == "kontra":
                cases = list(set(filter(lambda x: x != GrammarCase.WOLACZ, grammar_cases)))
            else:
                cases = list(set(filter(lambda x: x not in [GrammarCase.MIANOWNIK, GrammarCase.WOLACZ],
                                        grammar_cases)))
            if len(cases) > 2:
                # Skip, this is too confusing word
                continue
            elif len(cases) > 1:
                for case in cases:
                    prepositions_stats[preposition][case] += 1
            elif len(cases) == 1:
                prepositions_stats[preposition][cases[0]] += 10
            for case in cases:
                samples[preposition][case].append(noun_orig)
    return prepositions_stats, samples
