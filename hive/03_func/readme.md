### 文件说明：
- UDF
	- create_table_udtf.sql	udtf的建表语句
	- udtf.data	udtf的数据
	- HiveUppercase.java	UDF的函数
	- HiveExplode.java	UDTF的函数
	- pom.xml	jar包的pom文件
	- com.albert.hive.func-1.0-SNAPSHOT.jar	函数的jar包
- transform
	- transform.awk	transform的awk形式
	- transform.py	transform的python形式
	- trans_map.py	wordCount的map脚本
	- trans_red.py	wordCount的reduce脚本

### UDF UDTF前提
将使用的jar包添加到hive中

	hive> add jar /usr/local/src/learn/albert/18_hive_func/com.albert.hive.func-1.0-SNAPSHOT.jar;

# 一、UDF函数
## 1.UDF:
一进一出

	hive> create temporary function upper_func as 'HiveUppercase';

	hive> select movieid,title,upper_func(title) from movie_table limit 5;

## 2.UDTF:
一进多出

	hive> LOAD DATA LOCAL INPATH '/usr/local/src/learn/albert/18_hive_func/udtf.data' OVERWRITE INTO TABLE udtf_table;

	hive> create temporary function explode_func as 'HiveExplode';

	hive> select explode_func(id_score) from udtf_table;

## 3.UDAF:
多进一出


### <font color=red>注意：当使用temporary时，断开连接，函数被清空，需再次添加</font>

# 二、transform:
### 基本测试

本地测试

	echo "a b c" | awk -f transform.awk
	echo "a	b	c" | python transform.py

集群测试

	hive> add file /usr/local/src/learn/albert/18_hive_func/transform.awk;

	hive> select transform(movieid, title) using 'awk -f transform.awk' as (uuu) from movie_table limit 10;

### wordCount

### 1.数据准备

	# 存储结果表
	hive> CREATE TABLE word_count_res(
		> word STRING,
		> count STRING
		> );
	# 原始数据表
	hive> CREATE TABLE word_count_doc(
		> data STRING
		> );
	# 导入数据
	hive> LOAD DATA LOCAL INPATH '/usr/local/src/learn/albert/16_pyspark_test/The_Man_of_Property.txt' OVERWRITE INTO TABLE word_count_doc;

### 2.MR
	hive> add file /usr/local/src/learn/albert/18_hive_func/trans_map.py;
	hive> add file /usr/local/src/learn/albert/18_hive_func/trans_red.py;

	hive> select transform(wc.word, wc.count) using 'python trans_red.py' as w, c
		> from
		> (select transform(data) using 'python trans_map.py' as word, count from word_count_doc cluster by word) wc
		> limit 10;

### 3.存储结果

	hive> insert overwrite table word_count_res
		> select transform(wc.word, wc.count) using 'python trans_red.py' as w, c
		> from
		> (select transform(data) using 'python trans_map.py' as word, count from word_count_doc cluster by word) wc
		> ;

## <font color=red>注意引号</font>

### 没有引号

- add file /path/file_name.txt
- add jar /path/file_name.txt

### 有引号

- LOAD DATA LOCAL INPATH '/path/file_name.txt' OVERWRITE INTO TABLE table_name;