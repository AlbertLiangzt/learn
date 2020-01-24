#!/usr/local/bin/python

import sys

for line in sys.stdin:
	ss = line.strip().split('\t')
	if len(ss) != 2:
		continue
	file_name, file_content = ss
	word_list = file_content.strip().split(' ')
	
	word_set = set(word_list)

	for word in word_set:
		print '\t'.join([word, '1'])

