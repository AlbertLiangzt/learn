#!/usr/local/python/bin
# --coding:utf-8--

music_meta_data = './data/music_meta.data'
user_action_data = './data/user_watch_pref.sml'
user_profile_data = './data/user_profile.data'

output_file = "./data/1_merge.data"

out_file = open(output_file, "w")

# 过滤物品元数据
item_info_dic = {}
with open(music_meta_data, "r") as fd:
    for line in fd:
        ss = line.strip().split("\001")
        if len(ss) != 6:
            continue
        itemid, name, desc, time, language, tag = ss
        item_info_dic[itemid] = "\001".join([name, desc, time, language, tag])

# 过滤用户数据
user_info_dic = {}
with open(user_profile_data, "r") as fd:
    for line in fd:
        ss = line.strip().split(",")
        if len(ss) != 5:
            continue
        userid, gender, age, salary, location = ss
        user_info_dic[userid] = "\001".join([gender, age, salary, location])

# 过滤用户行为数据
# 将物品数据与用户数据进行合并
with open(user_action_data, "r") as fd:
    for line in fd:
        ss = line.strip().split("\001")
        if len(ss) != 4:
            continue
        userid, itemid, listen_time, click_time = ss

        if userid not in user_info_dic:
            continue
        if itemid not in item_info_dic:
            continue

        out_file.write(
            "\001".join([userid, itemid, listen_time, click_time,
                         user_info_dic[userid],
                         item_info_dic[itemid]]))
        out_file.write("\n")

out_file.close()
