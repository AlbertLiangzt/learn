#!/usr/bin/python
# -*- coding: utf-8 -*

import sys

cur_item = None
sum = 0.0

for line in sys.stdin:
    item_a_b, score = line.strip().split('\t')
    if not cur_item:
        cur_item = item_a_b

    # 切换item_a_b时，输出之前的item_a,item_b,score
    if cur_item != item_a_b:
        ss = cur_item.split('')
        if len(ss) != 2:
            continue
        item_a, item_b = ss
        print '%s\t%s\t%s' % (item_a, item_b, sum)

        sum = 0.0
        cur_item = item_a_b

    # 相似度计算公式，还差最后一步求和
    sum += float(score)

# 输出最后一个item_a_b
ss = cur_item.split('')
if len(ss) != 2:
    sys.exit()
item_a, item_b = ss
print '%s\t%s\t%s' % (item_a, item_b, sum)
