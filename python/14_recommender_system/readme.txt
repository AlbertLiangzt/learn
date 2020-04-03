data.rar需要先解压

推荐系统数据处理流程
1、数据预处理——过滤数据、合并数据
    IN->	用户画像数据
		user_profile.data	userid, gender, age, salary, location
	物品元数据
		music_meta.data	itemid, name, desc, time, language, tag
	用户行为数据
		user_watch_pref.sml	userid, itemid, listen_time, click_time
    OUT->	合并后数据
		1_merge.data	userid, itemid, listen_time, click_time, gender, age, salary, location, name, desc, time, language, tag
2、【召回】CB算法(CB,Content-based Recommendations)
	2.1token itemid score形式整理训练数据——利用jieba分词，对item name进行中文分词
		IN->	1_merge.data
		OUT->	name1_1	itemid_1	score1
			name1_2	itemid_1	score2
			desc1_1	itemid_1	score3
			desc1_2	itemid_1	score4
			tag1	itemid_1	score5
	2.2协同过滤（详见09_recommendation_algorithm），得到item-item的相似度(好几种方式跑下来的数据都是5.3g应该没问题吧)
		IN ->	token itemid score
		OUT->	itemid_1 itemid_2 simlar_score
	2.3数据格式化
		IN->	itemid_1 itemid_2 simlar_score
		OUT->	item_1	item_2:score1_item3:score2
	2.4灌数据——格式化后的数据写入redis
		2.4.1（本地测试）启动redis服务，另起终端，连接服务
		2.4.2用unix2dos（格式转换）
			unix2dos 2_3_cb_redis.data
		2.4.3将数据通过管道灌进redis
3、【召回】CF算法(User CF,User based Collaborative Filtering)
	3.1以userid itemid score形式整理训练数据
		IN->	1_merge.data
		OUT->	userid	itemid	score
	3.2协同过滤，得到基于cf的item-item的相似度（同2.2）
		IN->	userid	itemid	score
		OUT->	itemid_1 itemid_2 simlar_score
	3.3数据格式化（同2.3）
		IN->	itemid_1 itemid_2 simlar_score
		OUT->	item_1	item_2:score1_item3:score2
	3.4灌数据——格式化后的数据写入redis（同2.4）
		3.4.1（本地测试）启动redis服务，另起终端，连接服务
		3.4.2用unix2dos（格式转换）
			unix2dos 3_3_cf_redis.data 
		3.4.3将数据通过管道灌进redis
4、【排序】Sklearn
	4.1.将基础信息进行处理
			IN->1_merge.data	
				userid, itemid, listen_time, click_time, gender, age, salary, location, name, desc, time, language, tag
		4.1.1 用户特征
			OUT->userid	gender:weight_1	age:weight_2
		4.1.2 物品特征
			OUT->itemid	token_1:score_1	token_2:score_2...
		4.1.3 生成样本信息
			OUT->label	gender:weight_1	age:weight_2	token_1:score_1	token_2:score_2...
		4.1.4 生成样本id-name映射字典
			OUT->itemid	name
	4.2训练数据LR
		IN->	label	gender:weight_1	age:weight_2	token_1:score_1	token_2:score_2
		OUT->	model.w, model.b
		OUT->	true label
		OUT->	predict label
		OUT->	auc.data
	4.3评估模型(详见11_roc_auc_nb)
		IN->	label	prediction
		OUT->	roc/auc
		

step1
	python 1_merge_meta.py
step2
	python 2_1_cb_trains.py
	python 2_3_cb_format_redis.py
	cat 2_3_cb_redis.data | /usr/local/src/redis-2.8.3/src/redis-cli --pipe
step3
	python 3_1_cf_train.py
	python 3_3_cf_format_redis.py
	cat 3_3_cf_redis.data | /usr/local/src/redis-2.8.3/src/redis-cli --pipe
step4
	python 4_1_gen_samples.py
	python 4_2_lr_auc.py
	python 4_3_plot_roc.py


推荐系统实现流程
	1.解析请求：userid itemid（post、get）
	2.加载模型：加载排序模型model.w, model.b
	3.检索候选集合：利用cb、cf检索redis数据库
	4.获取用户特征：userid 4_1_user_feature.data
	5.获取物品特征：itemid 4_1_item_feature.data
	6.打分（逻辑回归、深度学习）、排序
	7.top-n过滤
	8.数据包装（itemid->name）、返回

step5
	get请求
	python 5_recommender_system.py 9999
	http://192.168.224.10:9999/?userid=00370d83b51febe3e8ae395afa95c684&itemid=3880409156
	post请求
	python 5_recommender_system_post.py 9999