# coding: utf-8
import sys

from markov import LettersMarkovChain, WordsMarkovChain
from ngrams import LettersNGramsStats, WordsNGramsStats, write_stats_to_file, read_stats_from_file

__author__ = "Michał Ciołczyk"

_POSSIBLE_USAGES = ['prepare', 'letters', 'words']
_INPUT = 'data/pap.txt'
_STATS_WORDS = 'data/words_%s.dat'
_STATS_LETTERS = 'data/letters_%s.dat'


def _usage(argv):
    print("Usage: python %s <action> <n>" % argv[0])
    print("\t where <action> is one of %s" % str(_POSSIBLE_USAGES))
    print("\t and <n> is length of n-grams")


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)
    if argc != 3:
        _usage(argv)
        exit(1)
    action = argv[1]
    n = int(argv[2])
    if action not in _POSSIBLE_USAGES:
        _usage(argv)
        exit(1)
    elif action == 'prepare':
        print("Preparing word n-grams...")
        words = WordsNGramsStats(n, _INPUT)
        print("Saving to file %s..." % (_STATS_WORDS % n))
        write_stats_to_file(words, _STATS_WORDS % n)
        print("Done")
        print("Preparing letter n-grams...")
        letters = LettersNGramsStats(n, _INPUT)
        print("Saving to file %s..." % (_STATS_LETTERS % n))
        write_stats_to_file(letters, _STATS_LETTERS % n)
        print("Done")
    else:
        filename = _STATS_WORDS % n if action == 'words' else _STATS_LETTERS % n
        print('Loading ngrams...')
        ngrams = read_stats_from_file(filename)
        print('Done')
        print('Generating output...')
        markov = WordsMarkovChain(ngrams, n) if action == 'words' else LettersMarkovChain(ngrams, n)
        while True:
            try:
                output = markov.generate()
                if action == 'letters' and len(output) < 5:
                    continue
                print(output)
                print()
                print("Press any key to continue, ctrl+d to end.")
                input()
            except UnicodeEncodeError:
                continue
            except EOFError:
                break
