# coding: utf-8
import codecs
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from operator import itemgetter

from ngrams import n_grams_stats
from stats import stats

_FILENAME = "data/potop.txt"
_STATS_FILENAME = "out/stats.csv"
_ENCODING = "utf-8"

__author__ = "Michał Ciołczyk"

_actions = ["ngrams", "words", "stats", "plots"]


def _usage(argv):
    print("Usage: python %s <action>" % argv[0])
    print("Action is one of: %s" % repr(_actions))
    exit(1)


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)
    if argc != 2:
        _usage(argv)
    action = argv[1]
    if action not in _actions:
        _usage(argv)
    if action == "words":
        print("Creating words stats...")
        stats, corpus_len = stats(_FILENAME, _ENCODING)
        print("\tDone")
        print("Saving results to file %s..." % _STATS_FILENAME)
        with codecs.open(_STATS_FILENAME, 'w', encoding=_ENCODING) as f:
            for rank, (word, count) in enumerate(sorted(stats.items(), key=itemgetter(1), reverse=True), 1):
                f.write('%s,%d,%d,%f\n' % (word, rank, count, count * 1. / corpus_len))
            print("\tDone")
    if action == "ngrams":
        print("Creating ngrams stats...")
        n_grams_stats(_FILENAME, _ENCODING)
        print("Done")
    if action == "stats":
        words = []
        hapax_legomena = []
        total_sum = 0
        half_sum = 0
        half_words = 0
        print("Reading stats file %s..." % _STATS_FILENAME)
        with codecs.open(_STATS_FILENAME, encoding=_ENCODING) as f:
            for line in f:
                word, rank, count, percent = line.split(',')
                rank = int(rank)
                count = int(count)
                percent = float(percent)
                words.append((word, rank, count, percent))
                if count == 1:
                    hapax_legomena.append(word)
                total_sum += count
        print("\tDone")
        print("Hapax legomena: %s" % ', '.join(hapax_legomena))
        print("Total hapax legomena count: %d" % len(hapax_legomena))
        print()
        for _, _, count, _ in words:
            if half_sum >= total_sum / 2:
                break
            half_sum += count
            half_words += 1
        print("50%% is covered by %d words (out of total %d words)" % (half_words, len(words)))
        print()
    if action == "plots":
        def zipf(x, k):
            return 1.0 * k / x


        def mandelbrot(x, B, d, P):
            return 1.0 * P / ((x + d) ** B)


        print("Reading stats file %s..." % _STATS_FILENAME)
        words = []
        with codecs.open(_STATS_FILENAME, encoding=_ENCODING) as f:
            for line in f:
                word, rank, count, percent = line.split(',')
                rank = int(rank)
                count = int(count)
                percent = float(percent)
                words.append((word, rank, count, percent))
        print("\tDone")

        xdata = np.array([i[1] for i in words])
        ydata = np.array([i[2] for i in words])

        zipf_popt, _ = curve_fit(zipf, xdata, ydata, p0=(1.0))
        mandelbrot_popt, _ = curve_fit(mandelbrot, xdata, ydata, p0=(1.0, 0.0, 2000.0))

        print("Zipf fit: k=%f" % tuple(zipf_popt))
        print("Mandelbrot fit: B=%f, d=%f, p=%f" % tuple(mandelbrot_popt))

        plt.plot(xdata, ydata, '-', label="Real data")
        plt.plot(xdata, zipf(xdata, *zipf_popt), '-', label="Zipf law")
        plt.plot(xdata, mandelbrot(xdata, *mandelbrot_popt), '-', label="Mandelbrot law")
        plt.xlabel("Rank")
        plt.ylabel("Frequency")
        plt.yscale('log')
        plt.ylim(ymin=0.1)
        plt.legend()
        plt.show()
        plt.savefig("out/plot.png")
