## 文件说明

- StormKafka.java storm的spout类
- PrinterBolt.java storm的bolt类
- run_storm_hbase.sh storm_hbase的执行方法

# 1.启动服务
## 1.1 flume kafka storm 

同<a href="https://blog.csdn.net/AlbertLiangzt/article/details/106596343">flume+kafka+storm</a>

## 1.2 hbase服务

hbase-0.98.6-hadoop2/bin/目录下

	./start-hbase.sh 

# 2.启动任务

	python /usr/local/src/apache-storm-0.9.3/bin/storm jar \
    	/usr/local/src/learn/albert/24_storm_extend/extend.jar \
    	stormHbase.StormKafka \

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200611002930589.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)