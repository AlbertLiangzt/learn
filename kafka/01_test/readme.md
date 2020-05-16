# 0.解压缩

	tar -zxvf kafka_2.11-0.10.2.1.tgz

# 1.修改参数

kafka_2.11-0.10.2.1/config目录下

server.properties文件

- master

		broker.id=0
		# 放开注释即可
		delete.topic.enable=true

- slave1

		broker.id=1
		# 放开注释即可
		delete.topic.enable=true

- slave2

		broker.id=2
		# 放开注释即可
		delete.topic.enable=true

# 2.服务测试

kafka_2.11-0.10.2.1/目录下

## 2.1 本地模式

### 2.1.1 启动服务

	./bin/kafka-server-start.sh config/server.properties


### 2.1.2 创建topic

--replication-factor 1 复本个数，不能超过机器个数

--partitions 1 partition个数

--topic topic_test topic名称

	./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic topic_test

### 2.1.3 查看topic列表

	./bin/kafka-topics.sh --list --zookeeper localhost:2181

### 2.1.4 查看topic描述

	./bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic topic_test 

![describe](https://img-blog.csdnimg.cn/20200515230553345.png)
表示的broker.id=0这个节点

### 2.1.5 删除topic

需要放开1中的注释
<font color=red>delete.topic.enable=true</font>

不然会报错<font color=red>Note: This will have no impact if delete.topic.enable is not set to true.</font>

![delete](https://img-blog.csdnimg.cn/20200515224133677.png)

	./bin/kafka-topics.sh --delete --zookeeper localhost:2181 --topic topic_test

### 2.1.6 发送、接受数据

- producer发送数据

		./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic topic_test

- consumer接收数据

		./bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic topic_test --from-beginning

![data](https://img-blog.csdnimg.cn/20200515224350266.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

## 2.2 集群模式

### 2.2.1 启动服务
同2.1.1

注意server.properties文件的broker.id

slave1、slave2的kafka_2.11-0.10.2.1/目录下执行

	./bin/kafka-server-start.sh config/server.properties

### 2.2.2 创建topic：
	
同2.1.2

replication-factor参数不能超过机器个数，否则会报错

	./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 5 --topic topic_test_cluster

### 2.2.3 查看topic列表

同2.1.3

	./bin/kafka-topics.sh --list --zookeeper localhost:2181

### 2.2.4 查看topic描述

同2.1.4

	./bin/kafka-topics.sh --describe --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic topic_test
![describe_cluster](https://img-blog.csdnimg.cn/20200515230632891.png)

# 3.producer、consumer

## 3.1 consumer group

- consumer_group.py代码
	
		#!/usr/local/bin/python
		from kafka import KafkaConsumer

		def main():
   			consumer = KafkaConsumer(b'topic_test_cluster', group_id=b'my_group_id', bootstrap_servers=['master:9092', 'slave1:9092', 'slave2:9092'], auto_offset_reset='earliest')
    	for msg in consumer:
        	print(msg)

		if __name__ == '__main__':
    		main()

- producer_group.py代码

		#!/usr/local/bin/python
		import time
		
		from kafka import SimpleProducer, KafkaClient
		from kafka.common import LeaderNotAvailableError
		
		def print_response(response=None):
		    if response:
		        print('Error: {0}'.format(response[0].error))
		        print('Offset: {0}'.format(response[0].offset))
		
		def main():
		    kafka = KafkaClient('localhost:9092')
		    producer = SimpleProducer(kafka)
		
		    topic = b'topic_test_cluster'
		    msg = b'Hello World, Hello Kafka'
		
		    try:
		        print_response(producer.send_messages(topic, msg))
		    except LeaderNotAvailableError:
		        time.sleep(1)
		        print_response(producer.send_messages(topic, msg))
		
		    kafka.close()
		
		if __name__ == '__main__':
		    main()

启动两个窗口

	python consumer_group.py

启动一个窗口

	python producer_group.py

![consumer_group](https://img-blog.csdnimg.cn/20200515234922311.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

## 3.2 发送数据给指定partition

- consumer_group.py代码
	
	同3.1 consumer_group.py
	
		#!/usr/local/bin/python
		from kafka import KafkaConsumer

		def main():
   			consumer = KafkaConsumer(b'topic_test_cluster', group_id=b'my_group_id', bootstrap_servers=['master:9092', 'slave1:9092', 'slave2:9092'], auto_offset_reset='earliest')
    	for msg in consumer:
        	print(msg)

		if __name__ == '__main__':
    		main()

启动两个窗口

	python consumer_group.py

启动一个窗口

	python producer_partition.py


### 3.2.2 partition分区的原则

- 指定partition的值

	- producer_partition_partition.py代码
		
		
			#!/usr/local/bin/python
		
			from kafka import KafkaProducer
		
			producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
		
			for i in range(0, 5):
		   		producer.send('topic_test_cluster', partition = i, value = ('%d' % i))
	    		producer.flush()


	- 方式

		会往指定的分区发送数据

	![在这里插入图片描述](https://img-blog.csdnimg.cn/20200516024832566.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

- 未指定partition的值，指定key

	- producer_partition_partition.py代码

			#!/usr/local/bin/python

			from kafka import KafkaProducer

			producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

			for i in range(0, 10):
    			producer.send('topic_test_cluster', key = ('%d' % i), value = b'keyValue')
   				producer.flush()
	
	- 方式
		
		kafka将key的hash值与topic的partition值进行取余，得到的值就是kafka生成的partition的值。

	![producer_partition_key](https://img-blog.csdnimg.cn/20200516024548853.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

- 未指定partition，未指定key

	- producer_partition_none.py代码

			#!/usr/local/bin/python

			from kafka import KafkaProducer

			producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

			for i in range(0, 10):
    			producer.send('topic_test_cluster', value = b'keyValue')
   				producer.flush()
	
	- 方式
	
		会随机生成一个整数key，以后每次生成都是在这个整数上加一。

	![producer_partition_none](https://img-blog.csdnimg.cn/20200516025601607.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

<font color=red>传输的值都是有序的，注意看时间戳！！！</br>
在各自的partition中有序</br></font>