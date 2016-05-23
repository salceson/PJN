# coding: utf-8
import codecs
import pickle
import re

from flection import basic_form
from graph import text_to_graph

__author__ = "Michał Ciołczyk"

_TEXT_SEPARATOR = re.compile('\n#[0-9]{6}\n')
_NOT_LETTERS = re.compile('[^a-ząćęłóńśżź]+')
_SPACES = re.compile('\s+')
_STOPWORDS_FILE = 'data/stopwords.txt'
_STOPWORDS_ENCODING = 'utf-8'


def _read_data(filename, encoding='utf-8'):
    with codecs.open(filename, encoding=encoding) as f:
        with codecs.open(_STOPWORDS_FILE, encoding=_STOPWORDS_ENCODING) as sw:
            stopwords = _SPACES.split(sw.read())
            texts = f.read()
            texts = re.split(_TEXT_SEPARATOR, texts)
            return [text.strip().lower() for text in texts], stopwords


def preprocess(filename, encoding='utf-8', k=1):
    print("Preprocessing data (k=%d)" % k)
    print("\tReading from file...")
    data, stopwords = _read_data(filename, encoding)
    print("\tStopwords and basic forms...")
    data = [_NOT_LETTERS.sub(' ', text) for text in data]
    data = [[basic_form(word) for word in _SPACES.split(text.lower())
             if len(word) > 0 and basic_form(word) not in stopwords] for text in data]
    print("\tGraphs...")
    graphs = []
    for i, text in enumerate(data):
        if i % 1000 == 0:
            print("\t\tProcessing text %d..." % i)
        graphs.append(text_to_graph(text, k))
    print("\tSaving data to file...")
    with open('data/graphs_%d.dat' % k, 'wb') as f:
        f.write(pickle.dumps(graphs))
