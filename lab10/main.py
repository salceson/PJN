# coding: utf-8
import pickle
import sys
from heapq import nlargest
from operator import itemgetter

from preprocess import build_prepositions_map, read_file, read_pap
from prepositions import prepositions_map_to_stats

__author__ = "Michał Ciołczyk"

_PAP_FILENAME = 'data/pap.txt'
_POTOP_FILENAME = 'data/potop.txt'
_PREPOSTITIONS_MAP = 'data/prepositions.dat'
_ACTIONS = ['preprocess', 'prepositions']


def _usage(argv):
    print('Usage: python %s <action>' % argv[0])
    print('\t where action is one of %r' % _ACTIONS)
    exit(1)


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) != 2:
        _usage(argv)
    action = argv[1]
    if action not in _ACTIONS:
        _usage(argv)
    if action == 'preprocess':
        texts = []
        texts += read_pap(_PAP_FILENAME)
        texts += read_file(_POTOP_FILENAME)
        build_prepositions_map(texts, _PREPOSTITIONS_MAP)
    if action == 'prepositions':
        with open(_PREPOSTITIONS_MAP, 'rb') as f:
            prepositions_map = pickle.loads(f.read())
        stats, samples = prepositions_map_to_stats(prepositions_map)


        def samples_for_case(preposition, case):
            all_samples_for_case = samples[preposition][case]
            if len(all_samples_for_case) <= 5:
                return ', '.join(all_samples_for_case)
            else:
                return ', '.join(all_samples_for_case[:5] + ['...'])


        for preposition, cases in stats.items():
            print('Przyimek: %s' % preposition)
            sum_cases_values = float(sum([cases[x] for x in cases]))
            cases_to_check = filter(lambda x: float(x[1]) / sum_cases_values * 100.0 > 10, cases.items())
            cases_to_present = nlargest(3, cases_to_check, key=itemgetter(1))
            case, value = cases_to_present[0]
            case_samples = samples_for_case(preposition, case)
            if float(value) / sum_cases_values * 100.0 > 80:
                print('\t%s: %f%% (praktycznie jedyny kandydat) [Samples: %s]' %
                      (case, float(value) / sum_cases_values * 100.0, case_samples))
            else:
                for case, value in cases_to_present:
                    case_samples = samples_for_case(preposition, case)
                    print('\t%s: %f%% [Samples: %s]'
                          % (case, float(value) / sum_cases_values * 100.0, case_samples))
