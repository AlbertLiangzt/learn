#!/usr/bin/python
# -*- coding: utf-8 -*

import sys
import math

cur_item = None
user_score_list = []

# f = open('map_1_out.data')

for line in sys.stdin:
# for line in f.readlines():
    ss = line.strip().split('\t')
    if len(ss) != 3:
        continue
    item, user, score = ss

    # 第一次进入赋值
    if cur_item == None:
        cur_item = item

    # 切换item时，输出之前的user，将item的score进行归一化操作
    if cur_item != item:
        sum = 0.0
        # 求出item对应的score的平方和
        for u_s in user_score_list:
            u, s = u_s
            sum += math.pow(s, 2)
        sum_sqrt = math.sqrt(sum)

        # 将score归一化
        for u_s in user_score_list:
            u, s = u_s
            print "%s\t%s\t%s" % (u, cur_item, float(s/sum_sqrt))
            user_score_list = []
        cur_item = item

    # 对同一个item，将user、score进行保存，以便进行归一化计算
    user_score_list.append((user, float(score)))

# 输出最后一个item值
sum = 0.0
## 求出item对应的score的平方和
for u_s in user_score_list:
    u, s = u_s
    sum += math.pow(s, 2)
sum_sqrt = math.sqrt(sum)

## 将score归一化
for u_s in user_score_list:
    u, s = u_s
    print "%s\t%s\t%s" % (u, cur_item, float(s / sum_sqrt))

