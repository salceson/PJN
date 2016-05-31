# coding: utf-8

from ctypes import *
from enum import Enum

__author__ = "Michał Ciołczyk"

_CLP_LIB_INSTANCE = CDLL('/usr/local/clp/lib/libclp.so')


class Word(object):
    @property
    def bform(self):
        raise NotImplementedError()

    def __str__(self):
        return self.bform

    def __repr__(self):
        return str(self)


class GrammarCase(Enum):
    MIANOWNIK = 1
    DOPELNIACZ = 2
    CELOWNIK = 3
    BIERNIK = 4
    NARZEDNIK = 5
    MIEJSCOWNIK = 6
    WOLACZ = 7
    LMN_MIANOWNIK = 8
    LMN_DOPELNIACZ = 9
    LMN_CELOWNIK = 10
    LMN_BIERNIK = 11
    LMN_NARZEDNIK = 12
    LMN_MIEJSCOWNIK = 13
    LMN_WOLACZ = 14

    @property
    def single(self):
        return GrammarCase((self.value - 1) % 7 + 1)

    def __str__(self):
        single = self.single
        if single == GrammarCase.MIANOWNIK:
            return 'Mianownik'
        if single == GrammarCase.DOPELNIACZ:
            return 'Dopelniacz'
        if single == GrammarCase.CELOWNIK:
            return 'Celownik'
        if single == GrammarCase.BIERNIK:
            return 'Biernik'
        if single == GrammarCase.NARZEDNIK:
            return 'Narzednik'
        if single == GrammarCase.MIEJSCOWNIK:
            return 'Miejscownik'
        if single == GrammarCase.WOLACZ:
            return 'Wołacz'
        raise KeyError(single)

    def __repr__(self):
        return str(self)


class GrammarPartOfSpeech(Enum):
    UNKNOWN = 0
    RZECZOWNIK = 1
    CZASOWNIK = 2
    PRZYMIOTNIK = 3
    LICZEBNIK = 4
    ZAIMEK = 5
    PRZYSLOWEK = 6
    WYKRZYKNIK = 7
    PRZYIMEK = 8
    SPOJNIK = 9
    NIEODMIENNY = 10
    SKROTOWIEC = 11


# noinspection PyCallingNonCallable,PyPep8Naming,PyShadowingBuiltins
class CLPWord(Word):
    def __init__(self, id):
        super(CLPWord, self).__init__()
        self._id = id

    @property
    def bform(self):
        bform = create_string_buffer(80)
        _CLP_LIB_INSTANCE.clp_form(c_int(self._id), bform)
        return bform.value.decode('utf-8')

    @property
    def forms(self):
        forms = create_string_buffer(2048)
        _CLP_LIB_INSTANCE.clp_forms(c_int(self._id), forms)
        return forms.value.decode('utf-8').split(':')[0:-1]

    @property
    def formsv(self):
        forms = create_string_buffer(2048)
        _CLP_LIB_INSTANCE.clp_formsv(c_int(self._id), forms)
        return forms.value.decode('utf-8').split(':')[0:-1]

    @property
    def pos(self):
        return GrammarPartOfSpeech(_CLP_LIB_INSTANCE.clp_pos(c_int(self._id)))

    @property
    def label(self):
        label = create_string_buffer(10)
        _CLP_LIB_INSTANCE.clp_label(c_int(self._id), label)
        return label.value

    def grammar_case(self, word):
        Array50 = c_int * 50
        out = Array50()
        num = c_int(0)
        _CLP_LIB_INSTANCE.clp_vec(c_int(self._id), bytes(word, 'utf-8'), out, byref(num))
        return list(set([GrammarCase(i).single for i in out[0:num.value]]))


# noinspection PyCallingNonCallable,PyPep8Naming,PyShadowingBuiltins
class CLPDictionary(object):
    def __init__(self):
        _CLP_LIB_INSTANCE.clp_init(1)

    def __getitem__(self, word):
        Array50 = c_int * 50
        ids = Array50()
        num = c_int(0)
        _CLP_LIB_INSTANCE.clp_rec(bytes(word, 'utf-8'), ids, byref(num))
        if num.value == 0:
            raise KeyError(word)
        return [CLPWord(id) for id in ids[0:num.value]]

    @property
    def version(self):
        ver = create_string_buffer(80)
        _CLP_LIB_INSTANCE.clp_ver(ver)
        return ver.value.decode('utf-8')

    def get(self, word, default=None):
        if default is None:
            default = []
        try:
            return self[word]
        except KeyError:
            return default
