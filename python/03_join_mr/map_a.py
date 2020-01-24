#!/usr/local/bin/python

import sys

for line in sys.stdin:
	ss = line.strip().split('\t')
	k = ss[0]
	v = ss[1]

	print '%s\t1\t%s' % (k, v)

