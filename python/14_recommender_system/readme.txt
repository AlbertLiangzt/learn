data.rar需要先解压

推荐系统
1、数据预处理——过滤数据、合并数据
    IN->	用户画像数据
		user_profile.data	userid, gender, age, salary, location
	物品元数据
		music_meta.data	itemid, name, desc, time, language, tag
	用户行为数据
		user_watch_pref.sml	userid, itemid, listen_time, click_time
    OUT->	合并后数据
		1_merge.data	userid, itemid, listen_time, click_time, gender, age, salary, location, name, desc, time, language, tag
2、【召回】CB算法
	2.1token itemid score形式整理训练数据——利用jieba分词，对item name进行中文分词
		IN->	1_merge.data
		OUT->	name1_1	itemid_1	score1
			name1_2	itemid_1	score2
			desc1_1	itemid_1	score3
			desc1_2	itemid_1	score4
			tag1	itemid_1	score5
	2.2协同过滤（详看09_recommendation_algorithm），得到item-item的相似度(好几种方式跑下来的数据都是5.3g应该没问题吧)
		IN ->	token itemid score
		OUT->	itemid_1 itemid_2 simlar_score
	2.3数据格式化
		IN->	itemid_1 itemid_2 simlar_score
		OUT->	item_1 -> item_2:score1_item3:score2
3、【召回】CF算法
4、【排序】Sklearn

python 1_merge_meta.py
pyrhon 2_1_cb_trains.py
python 2_3_cb_format_redis.py