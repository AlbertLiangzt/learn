#!/usr/local/bin/python

import sys

for line in sys.stdin:
	ss = line.strip().split('\t')
	print "_".join([ss[0].strip(), ss[1].strip()])
