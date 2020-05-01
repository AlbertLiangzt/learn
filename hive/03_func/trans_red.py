#!/usr/local/bin/python

import sys

last_key = None
last_count = 0

for line in sys.stdin:
	ss = line.strip().split("\t")
	if len(ss) != 2:
		continue
	key = ss[0].strip()
	count = ss[1].strip()

	if last_key and last_key != key:
		print "%s\t%d" % (last_key, last_count)
		last_key = key
		last_count = int(count)
	else:
		last_key = key
		last_count += int(count)

print "%s\t%d" % (last_key, last_count)
