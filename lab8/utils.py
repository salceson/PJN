# coding: utf-8
import codecs
import logging
import pickle
import re
from math import fsum, sqrt

from flection import basic_form
from gensim import corpora, models

__author__ = "Michał Ciołczyk"

_TEXT_SEPARATOR = re.compile('\n#[0-9]{6}\n')
_NOT_LETTERS = re.compile('[^a-ząćęłóńśżź]+')
_SPACES = re.compile('\s+')
_STOPWORDS_FILE = 'data/stopwords.txt'
_STOPWORDS_ENCODING = 'utf-8'

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def _read_data(filename, encoding='utf-8'):
    with codecs.open(filename, encoding=encoding) as f:
        with codecs.open(_STOPWORDS_FILE, encoding=_STOPWORDS_ENCODING) as sw:
            stopwords = _SPACES.split(sw.read())
            texts = f.read()
            texts = re.split(_TEXT_SEPARATOR, texts)
            return [text.strip().lower() for text in texts], stopwords


def preprocess_data(filename, encoding='utf-8'):
    print('Reading data...')
    data, stopwords = _read_data(filename, encoding)
    print('Done')
    print('Saving notes...')
    data_to_save = [text for text in data]
    with open('data/notes.dat', 'wb') as f:
        f.write(pickle.dumps(data_to_save))
    del data_to_save
    print('Done')
    print('Preprocessing data...')
    print('\tConverting to basic forms, applying stoplist...')
    data = [_NOT_LETTERS.sub(' ', text) for text in data]
    data = [[basic_form(word) for word in _SPACES.split(text.lower())
             if len(word) > 0 and basic_form(word) not in stopwords] for text in data]
    print('\tSaving preprocessed data')
    with open('data/preprocessed.dat', 'wb') as f:
        f.write(pickle.dumps(data))
    print('\tCreating dictionary...')
    dictionary = corpora.Dictionary(data)
    print('\tRemoving hapax legomena and words in at least 70% texts...')
    dictionary.filter_extremes(no_below=2, no_above=0.7, keep_n=200000)
    dictionary.compactify()
    print('\tSaving dictionary...')
    dictionary.save('data/dictionary.dat')
    print('Done')


def create_tfidf():
    print('Loading preprocessed data and dictionary...')
    with open('data/preprocessed.dat', 'rb') as f:
        data = pickle.loads(f.read())
    dictionary = corpora.Dictionary.load('data/dictionary.dat')
    print('Done')
    print('Calculating tf-idf...')
    bows = [dictionary.doc2bow(text) for text in data]
    tfidf = models.TfidfModel(bows)
    tfidf = tfidf[bows]
    print("Done")
    print("Saving tf-idf...")
    with open('data/tf-idf.dat', 'wb') as f:
        f.write(pickle.dumps(tfidf))
    print('Done')


def calculate_lsi():
    print('Reading tf-idf model and dictionary...')
    with open('data/tf-idf.dat', 'rb') as f:
        tfidf = pickle.loads(f.read())
    dictionary = corpora.Dictionary.load('data/dictionary.dat')
    print('Done')
    print('Calculating LSA model...')
    lsi_model = models.LsiModel(corpus=tfidf, num_topics=1000, id2word=dictionary)
    print("Done")
    print("Saving LSA model...")
    lsi_model.save('data/lsi.dat')
    print("Done")


def calculate_lda():
    print('Reading tf-idf model and dictionary...')
    with open('data/tf-idf.dat', 'rb') as f:
        tfidf = pickle.loads(f.read())
    dictionary = corpora.Dictionary.load('data/dictionary.dat')
    print('Done')
    print('Calculating LDA model...')
    lda_model = models.LdaModel(corpus=tfidf, num_topics=1000, id2word=dictionary)
    print("Done")
    print("Saving LDA model...")
    lda_model.save('data/lda.dat')
    print("Done")


def cosine_metric(vec1, vec2):
    vec1 = {k: v for k, v in vec1}
    vec2 = {k: v for k, v in vec2}
    keys = set(vec1.keys()) & set(vec2.keys())
    norm1 = sqrt(fsum([v * v for v in vec1.values()]))
    norm2 = sqrt(fsum([v * v for v in vec2.values()]))
    try:
        return 1. - fsum([vec1[key] * vec2[key] for key in keys]) / (norm1 * norm2)
    except ZeroDivisionError:
        return 1
