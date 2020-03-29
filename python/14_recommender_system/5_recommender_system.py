#!/usr/local/python/bin
# --coding:utf-8--

import web
import redis
import math

user_feature_file = ("./data/4_1_user_feature.data")
item_feature_file = ("./data/4_1_item_feature.data")
model_w_file = ("./data/4_2_model.w")
model_b_file = ("./data/4_2_model.b")

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
with open(item_feature_file, "r"):
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
        with open(model_w_file, "r") as fd:
            for line in fd:
                ss = line.strip().split(" ")
                if len(ss) != 3:
                    continue
                model_w_list.append(float(ss[2].strip()))
        with open(model_b_file, "\t") as fd:
            for line in fd:
                ss = line.strip().split(" ")
                if ss != 3:
                    continue
                model_b = float(ss[2].strip)

        # step 3:检索候选
        rec_item_merge = []
        # step 3.1:cf
        cf_info = "null"
        key = "_".join(["CF", req_itemid])
        if r.exists(key):
            cf_info = r.get(key)

        if len(cf_info) > 6:
            for cf_item_info in cf_info.strip().split("_"):
                item, score = cf_item_info.strip().split(":")
                rec_item_merge.append(item)
                
        # step 3.2:cb
        cb_info = "null"
        key = "_".join(["CB", req_itemid])
        if r.exists(key):
            cb_info = r.get(key)
        if len(cb_info) >6:
            for cb_item_info in cb_info.strip().split("_"):
                item,score = cb_item_info.strip().split(":")
                rec_item_merge.append(item)

class test:
    def GET(self):
        print web.input()
        return '222'


if __name__ == "__main__":
    app.run()
