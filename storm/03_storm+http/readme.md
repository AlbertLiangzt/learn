## 文件说明


# http+storm

## 1、测试

### 1.1 启动storm服务

apache-storm-0.9.3/conf/bin/目录下

- master

		python storm nimbus &
		python storm ui &
		python storm logviewer &

- slave1、slave2
	
		python storm supervisor &
		python storm logviewer &


### 1.2 简单测试

#### 1.2.1启动http端口
	
	nc -l 8808

#### 1.2.2启动测试类
	python /usr/local/src/apache-storm-0.9.3/bin/storm jar \
	    /usr/local/src/learn/albert/24_storm_extend/extend.jar \
	    stormHttp.HttpClientTest

### 1.3 web测试

#### 1.3.1 启动pyweb

	python 25_http_storm.py 8808

#### 1.3.2 启动测试类

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200607231654418.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)



## 
### 1.3 启动测试类

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200608164800486.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)



# 附：如果报错，存量topic格式不正确，删除、新建即可

kafka_2.11-0.10.2.1/目录下

	./bin/kafka-topics.sh --delete --zookeeper localhost:2181 --topic storm_kafka

	./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partition 5 --topic storm_kafka