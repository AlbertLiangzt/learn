#!/usr/local/python/bin
# --coding:utf-8--

import web
import redis
import math

user_feature_file = "./data/4_1_user_feature.data"
item_feature_file = "./data/4_1_item_feature.data"
item_id_name_file = "./data/4_1_item_id_to_name.data"
model_w_file = "./data/4_2_model.w"
model_b_file = "./data/4_2_model.b"

urls = (
    '/', 'index',
    '/test', 'test',
)

app = web.application(urls, globals())

# load user feature
user_feature_dict = {}
with open(user_feature_file, "r") as fd:
    for line in fd:
        ss = line.strip().split("\t")
        if len(ss) != 3:
            continue
        userid, feature_list_str = ss
        user_feature_dict[userid] = feature_list_str

# load item feature
item_feature_dict = {}
with open(item_feature_file, "r") as fd:
    for line in fd:
        ss = line.strip().split("\t")
        if len(ss) != 2:
            continue
        itemid, feature_list_str = ss
        item_feature_dict[itemid] = feature_list_str


class index:
    def GET(self):
        r = redis.Redis(host='master', port=6379, db=0)

        # sterp 1:解析请求
        params = web.input()
        req_userid = params.get("userid", "")
        req_itemid = params.get("itemid", "")

        # step 2:加载模型
        model_w_list = []
        model_b = 0
        with open(model_w_file, "r") as fd:
            for line in fd:
                ss = line.strip().split(" ")
                if len(ss) != 3:
                    continue
                model_w_list.append(float(ss[2].strip()))
        with open(model_b_file, "r") as fd:
            for line in fd:
                ss = line.strip().split(" ")
                if ss != 3:
                    continue
                model_b = float(ss[2].strip())

        # step 3:检索候选
        req_item_merge = []

        # step 3.1:cf
        cf_info = "null"
        key = "_".join(["CF", req_itemid])
        if r.exists(key):
            cf_info = r.get(key)

        if len(cf_info) > 6:
            for cf_item_info in cf_info.strip().split("_"):
                item, score = cf_item_info.strip().split(":")
                req_item_merge.append(item)

        # step 3.2:cb
        cb_info = "null"
        key = "_".join(["CB", req_itemid])
        if r.exists(key):
            cb_info = r.get(key)
        if len(cb_info) > 6:
            for cb_item_info in cb_info.strip().split("_"):
                item, score = cb_item_info.strip().split(":")
                req_item_merge.append(item)

        # step 4:获取用户特征
        user_features = ""
        if req_userid in user_feature_dict:
            user_features = user_feature_dict[req_userid]

        req_user_feature_dict = {}
        for user_fea_index in user_features.strip().split(" "):
            ss = user_fea_index.strip().split(":")
            if len(ss) != 2:
                continue
            fea = int(ss[0].strip())
            score = float(ss[1].strip())
            req_user_feature_dict[fea] = score

        # step 5:获取物品特征
        return_score_list = []
        for itemid in req_item_merge:
            if itemid in item_feature_dict:
                item_features = item_feature_dict[itemid]

                req_item_feature_dict = {}
                for item_fea_index in item_features.strip().split(" "):
                    ss = item_fea_index.strip().split(":")
                    if len(ss) != 2:
                        continue
                    fea = int(ss[0].strip())
                    score = float(ss[1].strip())
                    req_item_feature_dict[fea] = score

                wx_score = 0.
                # y = wx
                for fea, score in dict(req_user_feature_dict.items() + req_item_feature_dict.items()).items():
                    wx_score += (score * model_w_list[fea])
                # sigmoid : 1 / (1+exp(-wx))
                final_score = 1 / (1 + math.exp(wx_score + model_b))
                return_score_list.append((itemid, final_score))

        # step 6: 排序rank
        return_score_list = sorted(return_score_list, key=lambda x: x[1], reverse=True)

        # step 7:过滤filter
        filter_score_list = return_score_list[:10]

        # step 8:数据包装
        item_dict = {}
        with open(item_id_name_file, "r") as fd:
            for line in fd:
                item_id, item_name = line.strip().split("\t")
                item_dict[itemid] = item_name

        ret_list = []
        for tup in filter_score_list:
            req_item_name = item_dict[req_itemid]
            item_name = item_dict[tup[0]]
            item_rank_score = str(tup[1])
            ret_list.append(" -> ".join([req_item_name, item_name, item_rank_score]))

        ret = "\n".join(ret_list)

        return ret


class test:
    def GET(self):
        print web.input()
        return '222'


if __name__ == "__main__":
    app.run()
