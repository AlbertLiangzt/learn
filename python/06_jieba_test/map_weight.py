#!/usr/local/bin/python
# -*- coding:utf-8 -*

import sys
reload(sys)
sys.path.append('../../')
sys.setdefaultencoding('utf-8')

import jieba
import jieba.analyse

for line in sys.stdin:
	ss = line.strip().split('\t')
	music_id = ss[0]
	music_name = ss[1]

#	jieba分词
#        music_seg = jieba.cut(music_name, cut_all=False)
#        print ('%s\t%s\t%s' % (music_id, music_name, ' '.join(music_seg)))

#	jieba权重的计算
    	result_list = []
    	for x, w in jieba.analyse.extract_tags(music_name, withWeight=True):
        	result_list.append(':'.join([x, str(round(w, 3))]))
	print music_name + " ==> " +' '.join(result_list)



