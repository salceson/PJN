# coding: utf-8
import codecs
import pickle
import re
from collections import Counter, defaultdict
from heapq import nlargest
from math import log, fsum, sqrt
from operator import itemgetter

from flection import basic_form

__author__ = "Michał Ciołczyk"

_TEXT_SEPARATOR = re.compile('\n#[0-9]{6}\n')
_NOT_LETTERS = re.compile('[^a-ząćęłóńśżź]+')
_SPACES = re.compile('\s+')


def read_data(filename, encoding='utf-8'):
    with codecs.open(filename, encoding=encoding) as f:
        texts = f.read()
        texts = re.split(_TEXT_SEPARATOR, texts)
        return [text.strip().lower() for text in texts]


def prepare_data(filename, encoding='utf-8'):
    data = read_data(filename, encoding)
    data_to_save = {}
    term_frequencies = {}
    doc_frequencies = Counter()
    idfs = {}
    keywords = {}
    texts_num = len(data)
    print("Preparing data...")
    print("\tCalculating TF and DF...")
    for i, text in enumerate(data):
        data_to_save[i] = text
        text = _NOT_LETTERS.sub(' ', text)
        tf = Counter()
        # Calculate term frequencies for document
        for word in _SPACES.split(text):
            if not word:
                continue
            bform = basic_form(word)
            tf[bform] += 1
        term_frequencies[i] = tf
        # Update document frequencies
        for word in tf.keys():
            doc_frequencies[word] += 1
    print("\tTF and DF calculated")
    print("\t=> Saving notes")
    with open('data/notes.dat', 'wb') as f:
        f.write(pickle.dumps(data_to_save))
    del data_to_save
    print("\t=> Saving TF")
    with open('data/tfs.dat', 'wb') as f:
        f.write(pickle.dumps(term_frequencies))
    print("\t=> Saving DF")
    with open('data/dfs.dat', 'wb') as f:
        f.write(pickle.dumps(doc_frequencies))
    print("\tCalculating IDF...")
    for i in range(texts_num):
        idf = defaultdict(float)
        for word, word_tf in term_frequencies[i].items():
            idf[word] = word_tf * (log(texts_num / doc_frequencies[word]))
        normalized_idf = defaultdict(float)
        norm = sqrt(fsum([val * val for val in idf.values()]))
        for key, val in idf.items():
            normalized_idf[key] = val / norm
        idfs[i] = normalized_idf
    print("\tIDF calculated")
    print("\t=> Saving IDF")
    with open('data/idfs.dat', 'wb') as f:
        f.write(pickle.dumps(idfs))
    del term_frequencies
    del doc_frequencies
    print("\tCalculating keywords...")
    for i in range(texts_num):
        idf = idfs[i]
        keywords[i] = list(
            map(
                itemgetter(0),
                nlargest(min(10, int(0.25 * len(idf))), idf.items(), key=itemgetter(1))
            )
        )
    print("\tKeywords calculated")
    print("\t=> Saving keywords")
    with open('data/keywords.dat', 'wb') as f:
        f.write(pickle.dumps(keywords))
    del keywords
    print("Done")


def cosine_metric(vec1, vec2):
    vec1 = {k: v for k, v in vec1.items()}
    vec2 = {k: v for k, v in vec2.items()}
    keys = set(vec1.keys()) & set(vec2.keys())
    return 1. - fsum([vec1[key] * vec2[key] for key in keys])
