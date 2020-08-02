## 文件说明
- movies.csv 原始数据
- ratings.csv	原始数据
- ratings_2003-09.data	ratings.csv切割出的数据
- ratings_2003-10.data	ratings.csv切割出的数据
- ratings_2008-08.data	ratings.csv切割出的数据
- 01_create_rating_table.sql	内部表
- 02_create_movie_table_external.sql	外部表
- 03_create_table_partition.sql	分区表
- 04_create_table_bucket.sql	桶表

## 一、创建表
### 1.建表的两种方式

前提：HDFS必须有该文件，否则该表为空表

- 1.hive中执行sql
	
		# 内部表
		hive> CREATE TABLE rating_table(
			> userid string,
			> movieid string,
			> rating string,
			> ts string
			> )
			> row format delimited fields terminated by ','
			> stored as textfile
			> location '/hive_table';

		# 外部表
		hive> CREATE EXTERNAL TABLE movie_table(
			> movieid string,
			> title string,
			> genres string
			> )
			> row format delimited fields terminated by ','
			> stored as textfile;

- 2.hive命令执行
	
	xxx.sql就是1中的建表语句，写成文件形式

		hive -f xxx.sql


### 2.内部表、外部表区别

|| 内部表 | 外部表 |
|:-:|:-:|:-:|
| 定义 | 无<font color=red>external</font>修饰 | 被<font color=red>external</font>修饰 |
| 管理 | hive | hdfs |
| 存储位置 | 若指定路径：则为<font color=red>location</font>位置;</br>不指定路径：默认为/user/hive/warehouse</br> 配置路径hive-site.xml中<br>hive.metastore.warehouse.dir | 同内部表 |
| 删除表 | HDFS中文件被删除 | HDFS中文件不删除 |

## 二、导入数据 

### 1.从本地批量往table中灌数据：(此时HDFS上也有该文件)

	hive>LOAD DATA LOCAL INPATH '/usr/local/src/learn/albert/17_hive_test/ratings.csv' OVERWRITE INTO TABLE rating_table;

### 2.从HDFS批量往table中灌数据

	hive>LOAD DATA INPATH '/hive_table/movies.csv' OVERWRITE INTO TABLE movie_table

## 三、从Hive导出数据
### 1.导出到本地

	INSERT OVERWRITE LOCAL directory '/usr/local/src/learn/albert/17_hive_test/out_data' select userid, title from table_b;

### 2.导出到HDFS
	
	INSERT OVERWRITE directory '/hive_out_data' select userid, title from table_b;

## 四、分区partition
### 1.创建分区表

	hive> CREATE TABLE rating_table_partition(
		> userid string,
		> movieid string,
		> rating string
		> )
		> partitioned by(dt STRING)
		> row format delimited fields terminated by '\t'
		> lines terminated by '\n'
		
### 2.导入数据

	hive> LOAD DATA LOCAL INPATH '/usr/local/src/learn/albert/17_hive_test/ratings_2003-09.data' OVERWRITE INTO TABLE rating_table_partition partition(dt='2003-09');
	hive> LOAD DATA LOCAL INPATH '/usr/local/src/learn/albert/17_hive_test/ratings_2003-10.data' OVERWRITE INTO TABLE rating_table_partition partition(dt='2003-10');
	hive> LOAD DATA LOCAL INPATH '/usr/local/src/learn/albert/17_hive_test/ratings_2008-08.data' OVERWRITE INTO TABLE rating_table_partition partition(dt='2008-08');

### 3.查看分区数
	
	hive> show partitions rating_table_partition;

## 五、桶bucket

### 1.创建表

	hive> set hive.enforce.bucketing=true;
		> CREATE TABLE rating_table_bucket(
		> userid string,
		> movieid string,
		> rating string
		> )
		> clustered by (userid) INTO 16 buckets;

### 2.导入数据

	hive> FROM rating_table_partition
		> INSERT OVERWRITE TABLE rating_table_bucket
		> SELECT userid, movieid, rating;
		
### 3.采样

	hive> SELECT * FROM rating_table_bucket tablesample(bucket 1 out of 8 on userid) limit 5;

## <font color=red>注意：</font>
使用默认的Derby数据库作为元数据存储，会在当前工作目录下出现一个metastore_db的目录，该目录是在启动hive时由Derby创建。

切换到新的工作目录，Derby会“忘记”前一个目录下的元数据存储信息

- 第二次进入hive想看原来的数据，需要在上次建表的地方执行hive命令
	- 第一次在/user/local/tmp/下执行的hive命令，并建表插数据
	- 第二次只能在/user/local/tmp/下执行的hive命令，show tables;才会显示数据
	