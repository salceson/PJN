# coding: utf-8
import codecs
import pickle
import re
from collections import defaultdict

from clp import CLPDictionary, GrammarPartOfSpeech

__author__ = "Michał Ciołczyk"

_PAP_SPLITTER = re.compile('\n#[0-9]{6}\n')
_SENTENCE_SPLITTER = re.compile('\. \n?(?=[A-ZĄĆĘŁÓŃŚŻŹ])')
_NON_LETTERS = re.compile('[^a-ząćęłóńśżź]+')
_CLP = CLPDictionary()
_MAX_DISTANCE_FROM_PREPOSITION = 3


def read_pap(filename, encoding='utf-8'):
    with codecs.open(filename, encoding=encoding) as f:
        texts = f.read()
        texts = _PAP_SPLITTER.split(texts)
        return [text.strip() for text in texts]


def read_file(filename, encoding='utf-8'):
    with codecs.open(filename, encoding=encoding) as f:
        return [f.read().strip()]


# noinspection PyShadowingNames
def build_prepositions_map(texts, out_filename):
    print('Building prepositions map...')
    prepositions_map = defaultdict(set)
    for idx, text in enumerate(texts):
        if idx % 1000 == 999 or idx == len(texts) - 1:
            print('\tProcessing text #%d/%d' % (idx + 1, len(texts)))
        for sentence in _SENTENCE_SPLITTER.split(text):
            sentence = sentence.lower()
            sentence = _NON_LETTERS.sub(' ', sentence)
            sentence = sentence.strip()
            words = sentence.split(' ')
            word_idx = 0
            while word_idx < len(words):
                word = words[word_idx]
                clp_words = _CLP.get(word)
                clp_word = None
                for clp_word_sample in clp_words:
                    if clp_word_sample.pos is GrammarPartOfSpeech.PRZYIMEK:
                        clp_word = clp_word_sample
                        break
                if not clp_word:
                    word_idx += 1
                    continue
                continue_looking = True
                next_word_idx = word_idx + 1
                while continue_looking and next_word_idx < len(words) \
                        and (next_word_idx - word_idx) < _MAX_DISTANCE_FROM_PREPOSITION:
                    next_word = words[next_word_idx]
                    clp_next_words = filter(lambda w: w.pos is GrammarPartOfSpeech.RZECZOWNIK, _CLP.get(next_word))
                    for w in clp_next_words:
                        continue_looking = False
                        prepositions_map[word].add((next_word, w))
                    next_word_idx += 1
                word_idx += 1
    print('Done')
    with open(out_filename, 'wb') as f:
        f.write(pickle.dumps(prepositions_map))
