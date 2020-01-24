#!/usr/local/bin/python

import sys

base_count = 10000

for line in sys.stdin:
	ss = line.strip().split('\t')
	red_no, num, word = ss
	num = int(num) - base_count
	print '\t'.join([str(num), word])
