# coding: utf-8
import pickle
import sys
from heapq import nsmallest
from operator import itemgetter

from utils import preprocess

__author__ = "Michał Ciołczyk"

_DATA_FILE = 'data/pap.txt'
_ENCODING = 'utf-8'
_ACTIONS = ['preprocess', 'graph', 'notes', 'similar']


def _usage(argv):
    print("Usage: python %s <action> <k>" % argv[0])
    print("\tWhere action is one of: %s" % repr(_ACTIONS))
    print("\tAnd k is an integer")
    exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        _usage(sys.argv)
    action = sys.argv[1]
    k = 0
    if action not in _ACTIONS:
        _usage(sys.argv)
    try:
        k = int(sys.argv[2])
    except ValueError:
        _usage(sys.argv)
    if action == 'preprocess':
        preprocess(_DATA_FILE, encoding=_ENCODING, k=k)
    if action == 'graph':
        print("Loading graphs...")
        with open('data/graphs_%d.dat' % k, 'rb') as f:
            graphs = pickle.loads(f.read())
        while True:
            try:
                index = int(input('Enter note number (ctrl+d to end program): '))
                g = graphs[index]
                print("Writing image to out.png...")
                g.draw('out.png')
                print("Done")
                print()
            except (ValueError, KeyError):
                continue
            except (KeyboardInterrupt, EOFError):
                print()
                exit(0)
    if action == 'notes':
        print('Reading notes...')
        with open('data/notes.dat', 'rb') as f:
            data = pickle.loads(f.read())
        while True:
            try:
                index = int(input('Enter note number (ctrl+d to end program): '))
                print(data[index])
                print()
            except (ValueError, KeyError):
                continue
            except (KeyboardInterrupt, EOFError):
                print()
                exit(0)
    if action == 'similar':
        print("Loading graphs...")
        with open('data/graphs_%d.dat' % k, 'rb') as f:
            graphs = pickle.loads(f.read())
        while True:
            try:
                index = int(input('Enter note number (ctrl+d to end program): '))
                note = graphs[index]
                docs_similarities = [(i, g.get_metric(note)) for i, g in enumerate(graphs) if i != index]
                max_similarities = nsmallest(10, docs_similarities, key=itemgetter(1))
                print('10 most similar notes:')
                print(', '.join(['%d: %.2f' % (i, s) for i, s in max_similarities]))
                print()
            except (ValueError, KeyError):
                continue
            except (KeyboardInterrupt, EOFError):
                print()
                exit(0)
