# coding=utf-8
import os

import subprocess

__author__ = 'Michał Ciołczyk'

tests = {
    "test/de1.txt": "de",
    "test/de2.txt": "de",
    "test/de3.txt": "de",
    "test/pl1.txt": "pl",
    "test/pl2.txt": "pl",
    "test/pl3.txt": "pl",
    "test/fi1.txt": "fi",
    "test/fi2.txt": "fi",
    "test/fi3.txt": "fi",
    "test/it1.txt": "it",
    "test/it2.txt": "it",
    "test/it3.txt": "it",
    "test/en1.txt": "en",
    "test/en2.txt": "en",
    "test/en3.txt": "en",
    "test/es1.txt": "es",
    "test/es2.txt": "es",
    "test/es3.txt": "es",
}

ns = range(2, 16)

metrics = ["cosine", "euclidean", "max", "taxi"]

index = False  # On first run set to True

if index:
    print("Indexing...")

    for n in ns:
        print("\tProcessing n: %d..." % n)
        os.system("python index.py %d" % n)

    print("Indexing done")

texts_num = float(len(tests))
shorts_num = float(len([tests[test] for test in tests if test[-5] == "3"]))
long_num = texts_num - shorts_num

for metric in metrics:
    print("Processing metric: %s" % metric)
    with open("test/%s.txt" % metric, "w") as out_file:
        for n in ns:
            print("\tProcessing n: %d" % n)
            ok = 0
            shorts_ok = 0
            long_ok = 0
            for test in tests:
                p = subprocess.Popen(["python", "guess.py", test, metric, str(n)], stdout=subprocess.PIPE)
                result = str(p.stdout.read())[2:-3]
                print("\t\tTest: %s, expected = %s, actual = %s" % (test, tests[test], result))
                if tests[test] == result:
                    ok += 1
                    if test[-5] == "3":
                        shorts_ok += 1
                    else:
                        long_ok += 1
            print()
            all_percent = (ok / texts_num)
            short_percent = (shorts_ok / shorts_num)
            long_percent = (long_ok / long_num)
            print("\t\tAll ok: %f" % all_percent)
            print("\t\tShorts ok: %f" % short_percent)
            print("\t\tLong ok: %f" % long_percent)
            out_file.write("%d,%f,%f,%f\n" % (n, all_percent, short_percent, long_percent))
