# coding: utf-8
import sys

from preprocessing import process

__author__ = "Michał Ciołczyk"

_ACTIONS = ["preprocess", "dice", "cosine", "lcs"]
_INPUT_FILENAME = "data/lines.txt"
_PREPROCESSED_FILENAME = "data/preprocessed.txt"
_OUTPUT_PATTERN = "data/output_%s.txt"
_REFERENCE_FILENAME = "data/clusters.txt"
_DEBUG = True


def _usage():
    print("Usage: python %s <operation>" % args[0])
    print("Operation is one of: %s" % _ACTIONS)
    exit(1)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        _usage()
    action = args[1]
    if action not in _ACTIONS:
        _usage()
    if action == "preprocess":
        print("Preprocessing data...")
        print("\tInput: %s" % _INPUT_FILENAME)
        print("\tOutput: %s" % _PREPROCESSED_FILENAME)
        counter = 0
        with open(_INPUT_FILENAME) as input:
            with open(_PREPROCESSED_FILENAME) as output:
                for line in input:
                    preprocessed = process(line)
                    if _DEBUG and counter % 50 == 0:
                        print("\t\t%s => %s" % (line, preprocessed))
                    print(preprocessed, file=output)
                    counter += 1
