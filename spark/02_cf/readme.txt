CF
python版cf见09_recommendation_algorithm
1.归一化矩阵:
	1.1转置user item score，并且合并item
		IN	->	user	item	score
		OUT	->	item	list(user,score)
	1.2遍历每个item的score，求出平方和		
		IN	->	item (user_1, score_1)(user_2, score_2)(user_3, score_3)
		OUT	->	user	item	score_new
2.衍生pair对:
	2.1遍历所有的item，求出两两之间的分数score_new_1*score_new_2
		IN	->	user	item	score_new
		OUT	->	item_1	item_2	list(score_new_1*score_new_2=score_out2_1&2)
	2.2将所有item1-item2进行聚合(不同用户对item1-item2分别打分)
		IN	->	item_1	item_2	list(score_out2_1&2, score_out2_1&2)
3.生成结果:
	3.1取出所有item1-item2的分数，并相加score_out2_1&2+score_out2_1&2=score_sim_1&2
		IN	->	item_1	item_2	list(score_out2_1&2, score_out2_1&2)
		OUT	->	item_1	list[(item2, score_out31_1&2) (item3, score_out31_1&3)]
	3.2将分数排序、输出
		IN	->	item_1	list[(item2, score_sim_1&2) (item3, score_sim_1&3)]
		OUT	->	item_1	item_2:score_sim_1&2, item3:score_sim_1&3
