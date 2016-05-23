# coding: utf-8
import codecs
from collections import defaultdict

from plp import PLP

__author__ = "Michał Ciołczyk"

_FILENAME = "data/odm.txt"
_ENCODING = "windows-1250"
_basic_forms = defaultdict(list)
_initialized = False
_plp = PLP()
_SIE = ' się'


def _load_flection_map():
    global _initialized
    if not _initialized:
        with codecs.open(_FILENAME, 'r', encoding=_ENCODING) as f:
            for line in f:
                forms = line.rstrip('\n').split(', ')
                bform = forms[0]
                for form in forms:
                    _basic_forms[form].append(bform)
        for form, bforms in _basic_forms.items():
            _basic_forms[form] = list(set(bforms))
        _initialized = True


def _strip_sie(form):
    if form.endswith(_SIE):
        return form[:-len(_SIE)]
    return form


def basic_form(word):
    _load_flection_map()
    rec = _plp.rec(word)
    if rec:
        forms = list(set(_strip_sie(_plp.bform(id)) for id in rec))
    else:
        forms = _basic_forms.get(word)
    if not forms:
        return word
    else:
        try:
            return forms[0]
        except IndexError:
            return word
