#!/usr/local/bin/python
# --coding:utf-8--

input_file = "./data/3_2_cf_result.data"
output_file = "./data/3_3_cf_redis.data"

out_file = open(output_file, "w")

MAX_SIMILAR_SIZE = 100
PRE_STR = "CF_"
item_dic = {}

# item-item_list的形式
with open(input_file, "r") as fd:
    for line in fd:
        item_a, item_b, score = line.strip().split("\t")

        if item_a not in item_dic:
            item_dic[item_a] = []
        item_dic[item_a].append((item_b, score))

# SET CF_itemA itemB:scoreAB_itemC:scoreAC_itemD:scoreAD
for k, v in item_dic.items():
    key = PRE_STR + k

    list = sorted(v, key=lambda x: x[1], reverse=True)[:MAX_SIMILAR_SIZE]  # 取第二列降序
    val = "_".join([":".join([str(temp[0]), str(round(float(temp[1]), 6))]) for temp in list])

    out_file.write(" ".join(['SET', key, val]))
    out_file.write("\n")
out_file.close()
