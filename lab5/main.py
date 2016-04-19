# coding: utf-8
import sys
from time import sleep

from markov import LettersMarkovChain, WordsMarkovChain
from ngrams import LettersNGramsStats, WordsNGramsStats, write_stats_to_file, read_stats_from_file

__author__ = "Michał Ciołczyk"

_POSSIBLE_USAGES = ['prepare', 'letters', 'words']
_N = 2
_INPUT = 'data/pap.txt'
_STATS_WORDS = 'data/words.dat'
_STATS_LETTERS = 'data/letters.dat'


def _usage(argv):
    print("Usage: python %s <action>" % argv[0])
    print("\t where <action> is one of %s" % str(_POSSIBLE_USAGES))


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)
    if argc != 2:
        _usage(argv)
        exit(1)
    action = argv[1]
    if action not in _POSSIBLE_USAGES:
        _usage(argv)
        exit(1)
    elif action == 'prepare':
        print("Preparing word n-grams...")
        words = WordsNGramsStats(_N, _INPUT)
        print("Saving to file %s..." % _STATS_WORDS)
        write_stats_to_file(words, _STATS_WORDS)
        print("Done")
        print("Preparing letter n-grams...")
        letters = LettersNGramsStats(_N, _INPUT)
        print("Saving to file %s..." % _STATS_LETTERS)
        write_stats_to_file(letters, _STATS_LETTERS)
        print("Done")
    else:
        filename = _STATS_WORDS if action == 'words' else _STATS_LETTERS
        print('Loading ngrams...')
        ngrams = read_stats_from_file(filename)
        print('Done')
        print('Generating output (trigger keyboard interrupt to stop)...')
        markov = WordsMarkovChain(ngrams, _N) if action == 'words' else LettersMarkovChain(ngrams, _N)
        while True:
            try:
                output = markov.generate()
                if action == 'letters' and len(output) < 5:
                    continue
                print(output)
                print()
                sleep(5)
            except UnicodeEncodeError:
                continue
            except KeyboardInterrupt:
                break
