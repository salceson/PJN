# coding: utf-8
import pickle
import sys
from heapq import nlargest, nsmallest
from operator import itemgetter
from pprint import pprint

from gensim import corpora, models
from utils import calculate_lda, calculate_lsi, cosine_metric, preprocess_data, create_tfidf

__author__ = "Michał Ciołczyk"

_DATA_FILE = 'data/pap.txt'
_ENCODING = 'utf-8'
_ACTIONS = ['preprocess', 'preparetfidf',
            'preparelsa', 'preparelda',
            'notes', 'tfidf',
            'topicslsa', 'topicslda',
            'similarlsa', 'similarlda']
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
    if action == 'preparetfidf':
        create_tfidf()
    if action == 'preparelsa':
        calculate_lsi()
    if action == 'preparelda':
        calculate_lda()
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
    if action == 'tfidf':
        print('Reading tf-idf and dictionary...')
        with open('data/tf-idf.dat', 'rb') as f:
            tfidf = pickle.loads(f.read())
        dictionary = corpora.Dictionary.load('data/dictionary.dat')
        print('Done')
        while True:
            try:
                index = int(input('Enter note number (ctrl+d to end program): '))
                doc_tf_idf = [(dictionary[id], freq) for id, freq in tfidf[index]]
                print(doc_tf_idf)
                print()
            except (ValueError, KeyError):
                continue
            except (KeyboardInterrupt, EOFError):
                print()
                exit(0)
    if action == 'topicslsa':
        print('Reading LSA model and tf-idf...')
        lsi_model = models.LsiModel.load('data/lsi.dat')
        with open('data/tf-idf.dat', 'rb') as f:
            tfidf = pickle.loads(f.read())
        print('Done')
        while True:
            try:
                index = int(input('Enter note number (ctrl+d to end program): '))
                doc_tf_idf = tfidf[index]
                doc_projection = lsi_model[doc_tf_idf]
                topics = [(lsi_model.show_topic(x), weight)
                          for x, weight in nlargest(10, doc_projection, key=itemgetter(1))]
                pprint(topics)
                print()
            except (ValueError, KeyError):
                continue
            except (KeyboardInterrupt, EOFError):
                print()
                exit(0)
    if action == 'topicslda':
        print('Reading LDA model and tf-idf...')
        lda_model = models.LdaModel.load('data/lda.dat')
        with open('data/tf-idf.dat', 'rb') as f:
            tfidf = pickle.loads(f.read())
        print('Done')
        while True:
            try:
                index = int(input('Enter note number (ctrl+d to end program): '))
                doc_tf_idf = tfidf[index]
                doc_projection = lda_model[doc_tf_idf]
                topics = [(lda_model.show_topic(x), weight)
                          for x, weight in nlargest(10, doc_projection, key=itemgetter(1))]
                pprint(topics)
                print()
            except (ValueError, KeyError):
                continue
            except (KeyboardInterrupt, EOFError):
                print()
                exit(0)
    if action == 'similarlsa':
        print('Reading LSA model and tf-idf...')
        lsa_model = models.LsiModel.load('data/lsi.dat')
        with open('data/tf-idf.dat', 'rb') as f:
            tfidf = pickle.loads(f.read())
        print('Done')
        print('Projecting tf-idf onto LSA...')
        lsa_projections = lsa_model[tfidf]
        print('Done')
        while True:
            try:
                index = int(input('Enter note number (ctrl+d to end program): '))
                doc_tf_idf = tfidf[index]
                doc_projection = lsa_projections[index]
                docs_similarities = [(i, cosine_metric(doc_projection, p))
                                     for i, p in enumerate(lsa_projections)
                                     if i != index and cosine_metric(doc_projection, p) < _SIMILAR_THRESHOLD]
                max_similarities = nsmallest(10, docs_similarities, key=itemgetter(1))
                print('10 most similar notes:')
                print(', '.join(['%d: %.2f%%' % (i, s * 100) for i, s in max_similarities]))
                print()
            except (ValueError, KeyError):
                continue
            except (KeyboardInterrupt, EOFError):
                print()
                exit(0)
    if action == 'similarlda':
        print('Reading LDA model and tf-idf...')
        lda_model = models.LdaModel.load('data/lda.dat')
        with open('data/tf-idf.dat', 'rb') as f:
            tfidf = pickle.loads(f.read())
        print('Done')
        print('Projecting tf-idf onto LDA...')
        lda_projections = lda_model[tfidf]
        print('Done')
        while True:
            try:
                index = int(input('Enter note number (ctrl+d to end program): '))
                doc_tf_idf = tfidf[index]
                doc_projection = lda_projections[index]
                docs_similarities = [(i, cosine_metric(doc_projection, p))
                                     for i, p in enumerate(lda_projections)
                                     if i != index and cosine_metric(doc_projection, p) < _SIMILAR_THRESHOLD]
                max_similarities = nsmallest(10, docs_similarities, key=itemgetter(1))
                print('10 most similar notes:')
                print(', '.join(['%d: %.2f%%' % (i, s * 100) for i, s in max_similarities]))
                print()
            except (ValueError, KeyError):
                continue
            except (KeyboardInterrupt, EOFError):
                print()
                exit(0)
