tf：Term Frequency 词频
	tf = 某个词在文章中出现的次数/文章的总词数 
    或者
	tf = 某个词在文章中出现的次数/文章出现次数最多的词的次数
idf：Inverse Document Frequency 逆文本频率指数
	idf = log(语料的文档总数/(包含该词的文档数+1))

tf-idf = tf * idf

step 1 数据预处理
把所有文章的内容，全部收集到一个文件中
$ python convert.py input_tfidf_dir/ > idf_input.data

convert.py 实现逻辑：将input_tfidf_dir下的文件递归读取，每一篇文章读取成一段话，并在开头用序号标注，格式‘序号 文章内容’
注意：input_tfidf_dir目录下的文件都已经用空格分开每个词语了


step 2 计算idf
通过mr批量计算idf

map.py 实现逻辑：将每篇文章的词语进行去重操作，然后将所有的文章进行map处理
	cat idf_input.data | python map.py > map.result

normal_reduce.py 实现逻辑：将map.py中的结果进行reduce操作,统计出某个词语出现在多少篇文章中
	cat map.result | python normal_reduce.py > normal_reduce.result

idf.py 实现逻辑：将normal_reduce.py中的结果进行计算，得到idf
	cat normal_reduce.result | python idf.py > idf.result
