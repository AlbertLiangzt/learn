基于协同的推荐
实现方案——倒排式
		准备数据
	用户id, 物品id, 评分
        userid, itemid, score
        1,      101,    5
        1,      102,    3
        2,      101,    4
        2,      102,    3

实现步骤
1.归一化UI矩阵:
    需要将原来的得分进行归一化操作，重新输出userid, itemid, score_new
        map_1_normalized
                IN      ->      Line:   user, item, score
                OUT     ->      Key:    item
                                Value:  user, score
        reduce_1_normalized
                IN      ->      Key:    item
                                Value:  list((user, score))
                Out     ->      Key:    user
                                Value:  item, score_new

	输出：
	userid, itemid, score_new
	1,	101,	0.x
	2,	101,	0.x
	1,	102,	0.x
	2,	102,	0.x

2.衍生pair对——物品相似度
	map_2_pair:将第一步中的输出，作为输入，并重新进行分块
		IN	->	Key:    user
                                Value:  item, score_new
		OUT	->	Key:    user
                                Value:  item, score_new
	reduce_2_pair
                IN      ->      Key:    user
				Value:	list((item, score_new))
		OUT	->	Key_1: item_a	Value: score_new_a*score_new_b
				Key_2: item_b	Value: score_new_a*score_new_b

3.生成结果
	map_3_sum:将第二步中的输出，作为输入，并重新进行分块
		IN	->	Key:	item_a
				Value:	item_b, score_new_a*score_new_b
		OUT	->	Key:	<item_a, item_b>
				Value:	score_new_a*score_new_b

	reduce_3_sum:根据相似度计算公式Similarity formula,计算出item相似度
		IN	->	Key:    <item_a, item_b>
                                Value:  score_new_a*score_new_b
		OUT	->	Key:	item_a
				Value:	item_b, score_sum


step1.out 和 step2.out的数据，与集群中跑出来的数据是一样的（除了某些的顺序不一样，个数和分数都是一样的）
本地测试数据，step3.out比实际在集群中跑出来的数据小

cat music_uis.data | python map_1_normalized.py | sort -k1 | python reduce_1_normalized.py > step1.out

cat step1.out | python map_2_pair.py | sort -k1 | python reduce_2_pair.py > step2.out

cat step2.out | python map_3_sum.py | sort -k1 | python reduce_3_sum.py > step3.out


