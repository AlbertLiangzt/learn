#!/usr/local/bin/python
import sys

base_count = 10000

for line in sys.stdin:
	ss = line.strip().split('\t')
	num = int(ss[0]) + base_count
	word = ss[1]
	print '\t'.join([str(num), word])
