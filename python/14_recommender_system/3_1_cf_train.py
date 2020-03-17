#!/usr/local/bin/python
# --coding:utf-8--

input_file = "./data/1_merge.data"
output_file = "./data/3_1_cf_train.data"

out_file = open(output_file, "w")

# 分割merge的数据
# userid, itemid, listen_time, click_time,
# gender, age, salary, location,
# name, desc, time, language, tag
key_dic = {}
with open(input_file, "r") as fd:
    for line in fd:
        ss = line.strip().split("\001")
        # 用户行为
        userid = ss[0].strip()
        itemid = ss[1].strip()
        listen_time = ss[2].strip()
        click_time = ss[3].strip()
        # 用户画像
        gender = ss[4].strip()
        age = ss[5].strip()
        salary = ss[6].strip()
        location = ss[7].strip()
        # 物品元数据
        name = ss[8].strip()
        desc = ss[9].strip()
        time = ss[10].strip()
        language = ss[11].strip()
        tag = ss[12].strip()

        # 将userid_itemid, [liste_time, time]放入字段
        key = "_".join([userid, itemid])
        if key not in key_dic:
            key_dic[key] = []
        key_dic[key].append((int(listen_time), int(time)))

# 求出每个用户收听每首歌曲的时长比
for k, v in key_dic.items():
    tem_listen_time = 0
    tem_time = 0

    for v_time in v:
        tem_listen_time += v_time[0]
        tem_time += v_time[1]

    score = float(tem_listen_time) / float(tem_time)
    userid, itemid = k.strip().split('_')

    out_file.write("\t".join([userid, itemid, str(score)]))
    out_file.write("\n")

out_file.close()
