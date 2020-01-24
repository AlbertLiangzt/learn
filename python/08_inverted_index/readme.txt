倒排索引
原理：
1.map——得到正排索引，将item分成多个token，计算出每个token的权重，将其分割
	name -> token1 token2 token3 
2.map——根据token获取到item
	token1 -> name
	token2 -> name
	token3 -> name
3.reduce聚合——将2中token-item进行聚合，获得一个token对应多个item
	token1 -> name name name


map_1_name_token.py
	测试 name -> token1weight1token2weight2

map_2_token_name.py
	测试 token -> name weight

run_map_1.sh
	测试map_1在集群中的使用
