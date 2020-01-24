#!/usr/local/bin/python

import sys

tem = ''

for line in sys.stdin:
	key, flag, value = line.strip().split('\t')
	if flag == '1':
		tem = value
	elif flag == '2' :
		print '%s\t%s\t%s' % (key, tem, value)
		tem = ''
#print '%s\t%s' % (key, value)
