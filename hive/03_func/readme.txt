
hive> add jar /usr/local/src/learn/albert/18_hive_func/com.albert.hive.func-1.0-SNAPSHOT.jar;



UDF:
hive> create temporary function upper_func as 'HiveUppercase';
hive> select movieid,title,upper_func(title) from movie_table limit 5;

UDTF:
一行变多行
hive> LOAD DATA LOCAL INPATH '/usr/local/src/learn/albert/18_hive_func/udtf.data' OVERWRITE INTO TABLE udtf_table;
hive> create temporary function explode_func as 'HiveExplode';
hive> select explode_func(id_score) from udtf_table;

注意：当使用temporary时，断开连接，函数被清空，需再次添加

hive> add file /usr/local/src/learn/albert/18_hive_func/trasform.awk
hive> select transform(movieid, title) using 'awk -f transform.awk' as (uuu) from movie_table limit 10;
