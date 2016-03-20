#!/usr/bin/env python3
# coding=utf-8
import codecs

__author__ = 'Michał Ciołczyk'

ENCONDING = "iso8859-2"
FILENAME = "data/formy.txt"


def get_data_contents():
    with codecs.open(FILENAME, 'r', ENCONDING) as f:
        for word in f:
            yield word.strip()
