#!/usr/local/bin/python
# -*- coding:utf-8 -*

import os
import sys

os.system('tar xvzf jieba.tar.gz > /dev/null')

reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append("./")

import jieba
import jieba.posseg
import jieba.analyse

for line in sys.stdin:
	ss = line.strip().split('\t')
	if len(ss) != 2:
		continue
	music_id = ss[0].strip()
	music_name = ss[1].strip()

	weight_list = []
	for x, w in jieba.analyse.extract_tags(music_name, withWeight = True):
		weight_list.append(''.join([x, str(w)]))	
	print '\t'.join([music_id, music_name, ''.join(weight_list)])

	# 这种方式得到的结果是一样的
	#tmp_list = []
	#for x, w in jieba.analyse.extract_tags(music_name, withWeight=True):
	#	tmp_list.append((x, float(w)))

	#final_token_score_list = sorted(tmp_list, key=lambda x: x[1], reverse=True)

	#print '\t'.join([music_id, music_name, ''.join([''.join([t_w[0], str(t_w[1])]) for t_w in final_token_score_list])])

