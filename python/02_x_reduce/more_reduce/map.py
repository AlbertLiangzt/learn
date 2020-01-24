#!/usr/local/bin/python

import sys

base_count = 10000

for line in sys.stdin:
	ss = line.strip().split('\t')
	num = int(ss[0]) + base_count
	word = ss[1]
	
	red_no = 1 
	if num < (10100 + 10000)/2:
		red_no = 0
	print '%s\t%s\t%s' % (red_no, num, word) 

