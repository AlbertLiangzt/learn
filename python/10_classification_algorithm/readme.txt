分类算法——朴素贝叶斯 (NaiveBeyesian Classification NB)
原理
	朴素贝叶斯分类
	1.将80%的文章作为训练集，将20%的文章作为训练集
		1.1将文章按照文件名分类
		1.2将文章切割成词组
		1.3将文章中的词记录在词典中，形成“词-id”一一对应的形式
		1.4将原文章以id的形式输出
		OUT	->	训练集	文章类型 id_1 id_2 id_3 ... 文件名
					文章类型 id_4 id_5 id_6 ... 文件名
					...
				测试集	文章类型 id_1 id_2 id_3 ... 文件名
                		        文章类型 id_4 id_5 id_6 ... 文件名
                        		...
	
	2.利用训练集，得到一个模型
		OUT	->	文章类型	文章先验概率	词语默认概率	文章类型
				文章类型(未输出)	词语id	最大似然估计


	3.利用测试集，评估模型效果

实现步骤
	python DataConvert.py data/ nb_data

	python NB.py 1 nb_data.train model

	python NB.py 0 nb_data.test model out




