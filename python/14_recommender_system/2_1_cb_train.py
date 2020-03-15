#!/usr/local/bin/python
# --coding:utf-8--

import jieba.analyse
import sys

# 早期版本可以直接sys.setdefaultencoding('utf-8')，新版本需要先reloa
reload(sys)
sys.setdefaultencoding('utf-8')

input_file = "./data/1_merge.data"
output_file = "./data/2_1_cb_train.data"
idf_file = "./data/idf.txt"

out_file = open(output_file, "w")

# 初始化权重
RATIO_FOR_NAME = 0.9
RATIO_FOR_DESC = 0.1
RATIO_FOR_TAGS = 0.05

# 读取idf为字典
idf_dic = {}
with open(idf_file, "r") as fd:
    for line in fd:
        token, idf_score = line.strip().split(" ")
        idf_dic[token] = idf_score

# 分割merge的数据
# userid, itemid, listen_time, click_time,
# gender, age, salary, location,
# name, desc, time, language, tag
itemid_set = set()
with open(input_file, "r") as fd:
    for line in fd:
        ss = line.strip().split("\001")
        userid = ss[0].strip()
        itemid = ss[1].strip()
        # 用户行为数据
        listen_time = ss[2].strip()
        click_time = ss[3].strip()
        # 用户画像数据
        gender = ss[4].strip()
        age = ss[5].strip()
        salary = ss[6].strip()
        location = ss[7].strip()
        # 物品数据
        name = ss[8].strip()
        desc = ss[9].strip()
        time = ss[10].strip()
        language = ss[11].strip()
        tags = ss[12].strip()

        # itemid去重
        if itemid not in itemid_set:
            itemid_set.add(itemid)
        else:
            continue

        # 对name desc tag分词
        token_dic = {}
        for a in jieba.analyse.extract_tags(name, withWeight=True):
            token = a[0]
            score = float(a[1])
            token_dic[token] = score * RATIO_FOR_NAME

        for a in jieba.analyse.extract_tags(desc, withWeight=True):
            token = a[0]
            score = float(a[1])
            if token in token_dic:
                token_dic[token] += score * RATIO_FOR_DESC
            else:
                token_dic[token] = score * RATIO_FOR_DESC

        for tag in tags.strip().split(','):
            if tag not in idf_dic:
                continue
            else:
                if tag in token_dic:
                    token_dic[token] += float(idf_dic[tag]) * RATIO_FOR_TAGS
                else:
                    token_dic[token] = float(idf_dic[tag]) * RATIO_FOR_TAGS

        for k, v in token_dic.items():
            token = k.strip()
            score = str(v)
            out_file.write(",".join([token, itemid, score]))
            out_file.write("\n")

out_file.close()
