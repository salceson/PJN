#!/usr/bin/env python3
# coding=utf-8
import codecs
import os
import re
import sys
from collections import Counter
from glob import iglob

from n_grams import n_grams_from_data

__author__ = 'Michał Ciołczyk'

files_encondings = {
    "data/Harry Potter 1 Sorcerer's_Stone.txt": "ascii",
    "data/Harry Potter 2 Chamber_of_Secrets.txt": "ascii",
    "data/Harry Potter 3 Prisoner of Azkaban.txt": "ascii",
    "data/Harry Potter 4 and the Goblet of Fire.txt": "iso-8859-1",
    "data/spanish.txt": "iso-8859-9",
    "data/spanish1.txt": "iso-8859-9",
    "data/finnish.txt": "iso-8859-9",
    "data/finnish1.txt": "iso-8859-9",
    "data/2momm10.txt": "iso-8859-1",
    "data/4momm10.txt": "iso-8859-1",
    "data/5momm10.txt": "iso-8859-1",
    "data/8momm10.txt": "iso-8859-1",
    "data/54.txt": "iso-8859-9",
    "data/q.txt": "iso-8859-9",
    "data/polski.txt": "windows-1250",
    "data/polski2.txt": "windows-1250",
    "data/polski3.txt": "windows-1250",
}

files_languages = {
    "data/Harry Potter 1 Sorcerer's_Stone.txt": "en",
    "data/Harry Potter 2 Chamber_of_Secrets.txt": "en",
    "data/Harry Potter 3 Prisoner of Azkaban.txt": "en",
    "data/Harry Potter 4 and the Goblet of Fire.txt": "en",
    "data/spanish.txt": "es",
    "data/spanish1.txt": "es",
    "data/finnish.txt": "fi",
    "data/finnish1.txt": "fi",
    "data/2momm10.txt": "de",
    "data/4momm10.txt": "de",
    "data/5momm10.txt": "de",
    "data/8momm10.txt": "de",
    "data/54.txt": "it",
    "data/q.txt": "it",
    "data/polski.txt": "pl",
    "data/polski2.txt": "pl",
    "data/polski3.txt": "pl",
}

remove_not_letters = re.compile("[^a-z\s]")


def index_file(filename, n):
    with codecs.open(filename, 'r', files_encondings.get(filename, 'utf-8')) as f:
        return n_grams_from_data(f.read(), n)


def save_index(stat, filename):
    with open(filename, "w") as f:
        for key in stat:
            f.write("%s %d\n" % (key, stat[key]))


def corpus_stats(data_dir, out_dir, n):
    for filename in iglob(os.path.join(data_dir, "*.txt")):
        print("Processing file %s..." % filename)
        stat = index_file(filename, n)
        save_index(stat, os.path.join(out_dir, "%s_%d.txt" % (filename.split('/')[-1], n)))


def lang_stats(data_dir, out_dir, n, lang):
    lang_stat = Counter()
    for filename in iglob(os.path.join(data_dir, "*.txt")):
        if files_languages.get(filename, "nope") != lang:
            continue
        corpus_stats_filename = os.path.join(out_dir, "%s_%d.txt" % (filename.split('/')[-1], n))
        with open(corpus_stats_filename) as f:
            for line in f:
                key, count = line.split(' ')
                count = int(count)
                lang_stat[key] += count
    save_index(lang_stat, os.path.join(out_dir, "lang_%s_%d.txt" % (lang, n)))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: %s n" % sys.argv[0])
        exit(1)
    languages = ["en", "es", "fi", "de", "pl", "it"]
    data_dir = "data/"
    out_dir = "out/"
    n = int(sys.argv[1])

    corpus_stats(data_dir, out_dir, n)

    for lang in languages:
        print("Processing language %s..." % lang)
        lang_stats(data_dir, out_dir, n, lang)
