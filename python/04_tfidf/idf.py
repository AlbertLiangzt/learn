#!/usr/local/bin/python
# -*- coding: UTF-8 -*

import sys,math

# idf = log(文档总数/包含该词的文档数)

file_sum = 508

for line in sys.stdin:
	ss = line.strip().split('\t')
	if len(ss) != 2:
		continue
	word = ss[0]
	num = int(ss[1])
	idf = math.log(float(file_sum) / (float(num) + 1.0))
	print '%s\t%s' % (word, idf)
