#!/usr/local/bin/python
# --coding:utf-8--

import jieba.analyse

input_file = "./data/1_merge.data"
output_file = "./data/4_1_samples.data"

output_user_feature = "./data/4_1_user_feature.data"
output_item_feature = "./data/4_1_item_feature.data"
output_item_id_to_name = "./data/4_1_item_id_to_name.data"


# IN->userid, itemid, listen_time, click_time, gender, age, salary, location, name, desc, time, language, tag
# OUT->
# base_sample_list
# user_info_set 过滤重复的用户
# item_info_set 过滤重复的物品
# item_name_to_id id-name
# item_id_to_name name-id
def gen_base_samples():
    base_sample_list = []
    user_info_set = set()
    item_info_set = set()
    item_name_to_id = {}
    item_id_to_name = {}

    with open(input_file, "r") as fd:
        for line in fd:
            ss = line.strip().split("\001")
            if len(ss) != 13:
                continue

            userid = ss[0].strip()
            itemid = ss[1].strip()
            watch_time = ss[2].strip()
            total_time = ss[10].strip()

            # user info
            gender = ss[4].strip()
            age = ss[5].strip()
            user_feature = '\001'.join([userid, gender, age])

            # item info
            name = ss[8].strip()
            item_feature = '\001'.join([itemid, name])

            # label info
            label = float(watch_time) / float(total_time)
            if label >= 0.82:
                final_label = '1'
            elif label <= 0.3:
                final_label = '0'
            else:
                final_label = '0'

            item_id_to_name[itemid] = name
            item_name_to_id[name] = itemid

            base_sample_list.append([final_label, user_feature, item_feature])

            user_info_set.add(user_feature)
            item_info_set.add(name)

    return base_sample_list, user_info_set, item_info_set, item_name_to_id, item_id_to_name


# IN->userid gender age
# OUT->userid	gender:weight_1	age:weight_2
def gen_user_feature(user_info_set):
    user_feature_dic = {}
    for info in user_info_set:
        userid, gender, age = info.strip().split("\001")
        if gender == '男':
            target_gen = 1
        else:
            target_gen = 0

        gender_fea = ":".join([str(target_gen), "1"])

        if age == '0-18':
            target_age = 2
        elif age == '19-25':
            target_age = 3
        elif age == '26-35':
            target_age = 4
        elif age == '36-45':
            target_age = 5
        else:
            target_age = 6

        age_fea = ":".join([str(target_age), "1"])
        user_feature_dic[userid] = " ".join([gender_fea, age_fea])

    out_user_feature_file = open(output_user_feature, "w")
    for userid, user_feature in user_feature_dic.items():
        out_user_feature_file.write("\t".join([userid, user_feature]))
        out_user_feature_file.write("\n")
    out_user_feature_file.close()

    return user_feature_dic


# 通过jieba分词将name分成多个token
# IN->name
# OUT->itemid   token_1:score_1	token_2:score_2...
def gen_item_feature(item_info_set):
    item_token_score_dic = {}
    token_set = set()
    for name in item_info_set:
        token_score_list = []
        for token, score in jieba.analyse.extract_tags(name, withWeight=True):
            token_set.add(token)
            token_score_list.append((token, score))
        item_token_score_dic[name] = token_score_list

    # user_feature_offset = 10
    token_id_dic = {}
    for tok_index, tok_token in enumerate(list(token_set)):  # 将token组合为一个索引序列
        token_id_dic[tok_token] = tok_index

    item_feature_dic = {}
    for name, token_score_list in item_token_score_dic.items():
        tokenid_score_list = []
        for token, score in token_score_list:
            if token not in token_id_dic:
                continue
            # token_id = token_id_dic[token] + user_feature_offset
            token_id = token_id_dic[token]
            tokenid_score_list.append(":".join([str(token_id), str(score)]))
        item_feature_dic[name] = " ".join(tokenid_score_list)

    out_item_feature_file = open(output_item_feature, "w")
    for name, item_feature in item_feature_dic.items():
        if name not in item_name_to_id:
            continue
        itemid = item_name_to_id[name]
        out_item_feature_file.write("\t".join([itemid, item_feature]))
        out_item_feature_file.write("\n")
    out_item_feature_file.close()

    return item_feature_dic


# 过滤具有相同
# IN->
#   base_sample_list->label, user_feature, item_feature
#   user_feature_dic->userid	gender:weight_1	age:weight_2
#   item_feature_dic->itemid	token_1:score_1	token_2:score_2...
# OUT->label gender:weight_1 age:weight_2 token_1:score_1
def gen_final_samples(base_sample_list, user_feature_dic, item_feature_dic):
    out_final_samples_file = open(output_file, "w")
    for label, user_feature, item_feature in base_sample_list:
        userid = user_feature.strip().split("\001")[0]
        name = item_feature.strip().split("\001")[1]

        if userid not in user_feature_dic:
            continue
        if name not in item_feature_dic:
            continue

        out_final_samples_file.write("\t".join([label, user_feature_dic[userid], item_feature_dic[name]]))
        out_final_samples_file.write("\n")
    out_final_samples_file.close()


# IN->id name
# OUT->id  name
def gen_id_name_dic(item_id_to_name):
    out_item_id_to_name_file = open(output_item_id_to_name, "w")
    for id, name in item_id_to_name.items():
        out_item_id_to_name_file.write("\t".join([id, name]))
        out_item_id_to_name_file.write("\n")
    out_item_id_to_name_file.close()


if __name__ == "__main__":
    # step0 生成基础样本：基本样本列表、用户信息样本、物品信息样本、物品名称id对照、物品id名称对照
    base_sample_list, user_info_set, item_info_set, item_name_to_id, item_id_to_name = \
        gen_base_samples()

    # step1 生成用户特征 userid	gender:weight_1 age:weight_2
    user_feature_dic = gen_user_feature(user_info_set)

    # step2 生成物品特征
    item_feature_dic = gen_item_feature(item_info_set)

    # step3 生成最终样品信息
    gen_final_samples(base_sample_list, user_feature_dic, item_feature_dic)

    # step4 生成id-name映射字典
    gen_id_name_dic(item_id_to_name)
