#!/usr/local/bin/python

import sys

for line in sys.stdin:
	ss = line.strip().split(" ")
	for word in ss:
		print "%s\t1" %(word)
