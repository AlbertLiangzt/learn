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
	
	<font color=red>external</font>指表是外部的

	<font color=red>location</font>指定hive数据的路径

	<font color=red>row format delimited</font>分割行的字符

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
| 删除表 | HDFS中文件被删除 | HDFS中文件不删除,</br>但会删除描述表的元数据 |

严格意义上来说，hive只是管理外部表的这些目录和文件，并没有完全控制的权限

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
- 分区表能水平分散压力，将数据从物理上转移到和使用最频繁的而用户更近的地方，以实现其他目的。
- 分区表具有重要的性能优势，而且分区表也可以将数据以一种符合逻辑的方式进行组织，比如分层存储
- 比如以下的这张表，hive会创建好可以反应分区结构的子目录。比如：

	../rating_table_partition/dt=2018</br>
	../rating_table_partition/dt=2019</br>
	../rating_table_partition/dt=2020

- 外部表也能分区，用法与非外部表相同

### 1.创建分区表

	hive> CREATE TABLE rating_table_partition(
		> userid string,
		> movieid string,
		> rating string
		> )
		> partitioned by(dt STRING)
		> row format delimited fields terminated by '\t'
		> lines terminated by '\n';
		
### 2.导入数据

	hive> LOAD DATA LOCAL INPATH '/usr/local/src/learn/albert/17_hive_test/ratings_2003-09.data' OVERWRITE INTO TABLE rating_table_partition partition(dt='2003-09');
	hive> LOAD DATA LOCAL INPATH '/usr/local/src/learn/albert/17_hive_test/ratings_2003-10.data' OVERWRITE INTO TABLE rating_table_partition partition(dt='2003-10');
	hive> LOAD DATA LOCAL INPATH '/usr/local/src/learn/albert/17_hive_test/ratings_2008-08.data' OVERWRITE INTO TABLE rating_table_partition partition(dt='2008-08');

### 3.查看分区
- 查看分区数

		hive> show partitions rating_table_partition;

		OK
		dt=2003-09
		dt=2003-10
		dt=2008-08
		Time taken: 0.059 seconds, Fetched: 3 row(s)

- 查看分区键
	
		hive> describe rating_table_partiion;

		OK
		userid              	string              	                    
		movieid             	string              	                    
		rating              	string              	                    
		dt                  	string              	                    
			 	 
		# Partition Information	 	 
		# col_name            	data_type           	comment             
			 	 
		dt                  	string              	                    
		Time taken: 0.061 seconds, Fetched: 9 row(s)

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

## 六、查询数据

### 1.正常查询
进入hive客户端，执行查询操作
	
	$ hive
	hive> select * from movie_table limit 3;

	# 以下是执行结果
	OK
	movieId	title	genres
	1	Toy Story (1995)	Adventure|Animation|Children|Comedy|Fantasy
	2	Jumanji (1995)	Adventure|Children|Fantasy
	Time taken: 1.068 seconds, Fetched: 3 row(s)
	# 以上是执行结果

	hive> 

### 2.一次使用查询

只执行一次或多次查询（多个查询用“;”分割），查询完成立即退出

	$ hive -e "select * from movie_table limit 3"	

	# 以下是执行结果
	OK
	movieId	title	genres
	1	Toy Story (1995)	Adventure|Animation|Children|Comedy|Fantasy
	2	Jumanji (1995)	Adventure|Children|Fantasy
	Time taken: 1.406 seconds, Fetched: 3 row(s)
	# 以上是执行结果

	$ 

静默模式，删除“OK”“Time taken”等

	$ hive -S -e "select * from movie_table limit 3";

	# 以下是执行结果
	movieId	title	genres
	1	Toy Story (1995)	Adventure|Animation|Children|Comedy|Fantasy
	2	Jumanji (1995)	Adventure|Children|Fantasy
	# 以上是执行结果

	$ 

## 七、修改表

ALTER TABLE仅会修改表元数据，不会修改表数据

### 1、表名

	hive> ALTER TABLE table_old_name RENAME TO table_new_name;

### 2、表分区

- 增加表分区

		```sql
		ALTER TABLE log_table ADD IF NOT EXISTS
		PARTITION (year=2020, month=1, day=1) LOCATION '/logs/2020/01/01'
		PARTITION (year=2020, month=1, day=2) LOCATION '/logs/2020/01/02'
		PARTITION (year=2020, month=1, day=3) LOCATION '/logs/2020/01/03'
		...
		;
		```

- 修改/移动分区

		ALTER TABLE log_table PARTITION (year=2020, month=1, day=3) SET LOCATION '/logs/2019/11/13';

- 删除分区

		ALTER TABLE log_table DROP IF EXISTS PARTITION (year=2020, month=1, day=3);

	同理，外部表分区内数据不会被删除，内部表分区内数据会删除

### 3、列

- 修改列

		ALTER TABLE log_table CHANGE COLUMN col_old_name col_new_name STRING FIRST;

	<font color=blue>ALTER TABLE </font>log_table *# 修改的表*</br> 
	<font color=blue>CHANGE COLUMN</font> col_old_name col_new_name STRING *# 原列名，新列名 列类型*</br>
	<font color=blue>FIRST</font> *# 该列的位置*;

	列的位置可以使用<font color=blue>AFTER</font> col_name，移动到某列之后 

- 增加列

		ALTER TABLE log_table ADD COLUMNS (col_name_one STRING, col_name_two INT);

- 删除/替换列

	没有类似于mysql的<font color=blue>ALTER TABLE </font>table_name <font color=blue>DROP </font>col_name的功能。只能做替换

		原表 
		
			CREATE TABLE table_name(
				name STRING,
				id INT
			);

		删除id列

			ALTER TABLE table_name REPLACE COLUMNS (
				name STRING
			);
## <font color=red>注意：</font>
使用默认的Derby数据库作为元数据存储，会在当前工作目录下出现一个metastore_db的目录，该目录是在启动hive时由Derby创建。

切换到新的工作目录，Derby会“忘记”前一个目录下的元数据存储信息

- 第二次进入hive想看原来的数据，需要在上次建表的地方执行hive命令
	- 第一次在/user/local/tmp/下执行的hive命令，并建表插数据
	- 第二次只能在/user/local/tmp/下执行的hive命令，`show tables`才会显示数据
