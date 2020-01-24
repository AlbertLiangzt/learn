#!/usr/bin/python

import sys

for line in sys.stdin:
    user, item, score = line.strip().split('\t')
    print "%s\t%s\t%s" % (user, item, score)
