#!/usr/bin/python
# -*- coding: utf-8 -*

import sys
import math

cur_user = None
item_score_list = []

#f = open('step1_map2.out')

for line in sys.stdin:
# for line in f.readlines():
    user, item, score = line.strip().split('\t')
    # 第一次进入赋值
    if not cur_user:
        cur_user = user

    # 各个item两两比较的相似度打分情况
    if cur_user != user:

        # list的倒数第二位是i，倒数第一位是j
        for i in range(0, len(item_score_list)-1):
            for j in range(i+1, len(item_score_list)):
                item_a, score_a = item_score_list[i]
                item_b, score_b = item_score_list[j]
		# 输出一次，只会得到矩阵的1/2
                print "%s\t%s\t%s" % (item_a, item_b, float(score_a)*float(score_b))
                print "%s\t%s\t%s" % (item_b, item_a, float(score_a)*float(score_b))
        cur_user = user
        item_score_list=[]

    item_score_list.append((item, score))

# 输出最后一个user的得分
for i in range(0, len(item_score_list) - 1):
    for j in range(i + 1, len(item_score_list)):
        item_a, score_a = item_score_list[i]
        item_b, score_b = item_score_list[j]
	# 输出一次，只会得到矩阵的1/2
        print "%s\t%s\t%s" % (item_a, item_b, float(score_a) * float(score_b))
        print "%s\t%s\t%s" % (item_b, item_a, float(score_a) * float(score_b))
