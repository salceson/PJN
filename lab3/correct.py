# coding=utf-8

from heapq import nlargest
from operator import itemgetter
from time import time

from metric import levenshtein_metric
from utils import corpus_stats, error_stats, get_corrections

__author__ = "Michał Ciołczyk"

CORPUS = [
    "data/dramat.iso.utf8",
    "data/popul.iso.utf8",
    "data/proza.iso.utf8",
    "data/publ.iso.utf8",
    "data/wp.iso.utf8",
]

ERROR_FILE = "data/bledy.txt"
FORMS_FILE = "data/formy.txt"
FORMS_ENCODING = "iso-8859-2"
MAX_LENGTH_DIFFERENCE = 3
LAMBDA = 5
ALPHABET = 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'


def correct_word(word, corpus_stats, errors_stats, corrections):
    corrections = {
        correction: errors_stats[levenshtein_metric(word, correction, False)] * corpus_stats[correction] ** LAMBDA for
        correction in corrections if abs(len(word) - len(correction)) <= MAX_LENGTH_DIFFERENCE
        }
    return nlargest(10, corrections.items(), key=itemgetter(1))


def compute_possible_corrections(word, forms):
    return known([word], forms) or known(edits1(word), forms) or known_edits2(word, forms) or [word]


def known(words, forms):
    return set(w for w in words if w in forms)


def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in ALPHABET if b]
    inserts = [a + c + b for a, b in splits for c in ALPHABET]
    return set(deletes + transposes + replaces + inserts)


def known_edits2(word, forms):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in forms)


if __name__ == "__main__":
    print("Please wait, reading data files...")

    forms = get_corrections(FORMS_FILE, FORMS_ENCODING)
    corpus_statistics = corpus_stats(CORPUS, len(forms))
    error_statistics = error_stats(ERROR_FILE)

    print("Please enter words to correct them.")

    while True:
        try:
            word = input("> ")
            time1 = time()
            corrections = correct_word(
                word, corpus_statistics, error_statistics, compute_possible_corrections(word, forms)
            )
            time2 = time()
            print(corrections)
            print("Corrections: %s" % ', '.join(list(map(itemgetter(0), corrections))))
            print("Run for %s seconds." % (time2 - time1))
        except EOFError:
            break
