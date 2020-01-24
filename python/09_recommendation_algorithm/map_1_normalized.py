#!/usr/bin/python


import sys

for line in sys.stdin:
	ss = line.strip().split('\t')
	if len(ss) != 3:
		continue
	user, item, score = ss
	print "%s\t%s\t%s" % (item, user, score)
