#!/usr/bin/env python3
# coding=utf-8

import subprocess

__author__ = 'Michał Ciołczyk'

if __name__ == "__main__":
    words = ["pomidor", "pomdior", "dupeczka", "rozwiac", "abzzur", "teatruw"]
    interpreters = ["python3", "pypy3"]
    for interpreter in interpreters:
        print("Interpreter:", interpreter)
        for word in words:
            p = subprocess.Popen([interpreter, "correct.py", word], stdout=subprocess.PIPE)
            result = p.communicate()[0].decode("utf-8").replace("\n", "\n\t")
            print("\t%s" % str(result))
