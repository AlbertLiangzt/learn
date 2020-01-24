#!/usr/bin/python

import os
import sys

for line in sys.stdin:
	ss = line.strip().split('\t')
	if len(ss) != 3:
		continue
	music_id = ss[0].strip()
	music_name = ss[1].strip()
	music_token_list = ss[2].strip()

	for token_list in music_token_list.split(''):
		token, weight = token_list.strip().split('')
		print '\t'.join([token, music_name, weight])
