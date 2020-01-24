#!/usr/local/bin/python

import sys

tem_word = None
tem_num = 0

for line in sys.stdin:
	ss = line.strip().split('\t')

	if len(ss) != 2:
		continue	

	word, num = ss
	
	if tem_word == None:
		tem_word = word
	if word != tem_word:
		print '%s\t%s' % (tem_word, tem_num)
		tem_word = word
		tem_num = 0
	tem_num += int(num)
print '%s\t%s' % (word, tem_num)
	
