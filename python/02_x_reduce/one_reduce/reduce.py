#!/usr/local/bin/python

import sys

base_count = 10000

for line in sys.stdin:
	ss = line.strip().split('\t')
	num = int(ss[0])
	word = ss[1]
	print '%s\t%s' % (num-base_count, word)
