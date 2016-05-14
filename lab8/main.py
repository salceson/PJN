# coding: utf-8
import pickle
import sys
from functools import reduce

from flection import basic_form
from utils import calculate_lda, calculate_lsi, cosine_metric, preprocess_data, create_tfidf

__author__ = "Michał Ciołczyk"

_DATA_FILE = 'data/pap.txt'
_ENCODING = 'utf-8'
_ACTIONS = ['preprocess', 'tfidf', 'preparelsa', 'preparelda', 'file', 'search', 'search_keywords']
_SIMILAR_THRESHOLD = 0.4


def _usage(argv):
    print("Usage: python %s <action>" % argv[0])
    print("\tWhere action is one of: %s" % repr(_ACTIONS))
    exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        _usage(sys.argv)
    action = sys.argv[1]
    if action not in _ACTIONS:
        _usage(sys.argv)
    if action == 'preprocess':
        preprocess_data(_DATA_FILE, _ENCODING)
    if action == 'tfidf':
        create_tfidf()
    if action == 'preparelsa':
        calculate_lsi()
    if action == 'preparelda':
        calculate_lda()
    if action == 'file':
        file = input('Enter file: data/')
        with open('data/' + file, 'rb') as f:
            file_contents = pickle.loads(f.read())
        print('File read')
        while True:
            try:
                i = input('Enter index (ctrl+d to end program): ')
                try:
                    i = int(i)
                except:
                    pass
                try:
                    print(file_contents[i])
                except KeyError:
                    pass
            except (KeyboardInterrupt, EOFError):
                exit(0)
    if action == 'search_keywords':
        print('Reading data...')
        with open('data/keywords.dat', 'rb') as f:
            keywords = pickle.loads(f.read())
        print('Done')
        while True:
            try:
                search_terms = input('Enter keywords separated by space (ctrl+d to end program): ')
                search_terms = search_terms.split(' ')
                search_terms = list(map(lambda x: basic_form(x), search_terms))
                notes_found = []
                for i in range(len(keywords)):
                    show = reduce(lambda acc, x: acc and (x in keywords[i]), search_terms, True)
                    if show:
                        notes_found.append(str(i))
                print('Found notes numbers: ' + ', '.join(notes_found))
            except (KeyboardInterrupt, EOFError):
                exit(0)
    if action == 'search':
        print('Reading data...')
        with open('data/idfs.dat', 'rb') as f:
            idfs = pickle.loads(f.read())
        print('Done')
        notes_len = len(idfs)
        while True:
            try:
                note = input('Enter note number (max: %d, ctrl+d to end program): ' % notes_len)
                try:
                    note = int(note)
                    note_idf = idfs[note]
                except (ValueError, KeyError):
                    continue
                similar = []
                for i in range(len(idfs)):
                    if i == note:
                        continue
                    metric = cosine_metric(idfs[i], note_idf)
                    if metric < _SIMILAR_THRESHOLD:
                        similar.append('%d (%.3f%%)' % (i, metric * 100))
                print('Found similar notes numbers: ' + ', '.join(similar))
            except (KeyboardInterrupt, EOFError):
                exit(0)
