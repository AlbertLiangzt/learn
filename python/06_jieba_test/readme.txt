
test.py	测试jieba

map_segment.py 用jieba进行分词操作，将输入的一条语句，分解成多个词语
	这是一个神奇的故事	--->> 这是 一个 神奇 的 故事
	cat music_meta.txt.small | python map_segment.py > segment.result

map_weight.py 用jieba分词操作，并进行权重的计算 权重-tfidf
	cat music_meta.txt.small | python map_weight.py > weight.result

