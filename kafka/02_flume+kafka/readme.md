## 文件说明
接01_test

- consumer_flume_kafka.py	consumer
- flume_kafka_exec.properties	exec配置	
- flume_kafka_interceptor.properties	interceptor配置
# 4.flum+kafka

## 4.1服务准备kafka
- master、slave1、slave2服务

		./bin/kafka-server-start.sh config/server.properties

- 创建一个新的topic

		./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 5 --topic flume_kafka
		
- consumer服务

	consumer_kafka.py代码

		#!/usr/local/bin/python
		from kafka import KafkaConsumer
		
		def main():
			consumer = KafkaConsumer(b'flume_kafka', group_id=b'my_group_id', bootstrap_servers=['master:9092', 'slave1:9092', 'slave2:9092'], auto_offset_reset='earliest')
			for msg in consumer:
				print(msg)
		
		if __name__ == '__main__':
			main()

	启动服务

		python consumer_kafka.py

## 4.2启动flume

### 4.2.1exec

- flume_kafka_exec.properties代码
	
	apache-flume-1.6.0-bin/conf目录下

		# Name the components on this agent
		agent1.sources = source1
		agent1.sinks = sink1
		agent1.channels = channel1
		
		# Describe/configure the source
		agent1.sources.source1.type = exec
		agent1.sources.source1.command = tail -f /usr/local/src/learn/albert/21_flume/1.log
		
		# Describe the sink
		agent1.sinks.sink1.type = org.apache.flume.sink.kafka.KafkaSink
		agent1.sinks.sink1.brokerList  = master:9092
		agent1.sinks.sink1.topic = flume_kafka
		
		# Use a channel which buffers events in memory
		agent1.channels.channel1.type = memory
		agent1.channels.channel1.capacity = 1000
		agent1.channels.channel1.transactionCapacity = 100
		
		# Bind the source and sink to the channel
		agent1.sources.source1.channels = channel1
		agent1.sinks.sink1.channel = channel1


- 启动

	apache-flume-1.6.0-bin/目录下

		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_kafka_exec.properties --name agent1 -Dflume.root.logger=INFO,console

- 测试
		
	/usr/local/src/learn/albert/21_flume/目录下

	![在这里插入图片描述](https://img-blog.csdnimg.cn/20200517170858129.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

### 4.2.2interceptor

- flume_kafka_interceptor.properties代码
	
	apache-flume-1.6.0-bin/conf目录下

		# Name the components on this agent
		agent1.sources = source1
		agent1.sinks = sink1
		agent1.channels = channel1
		
		# Describe/configure the source
		agent1.sources.source1.type = http
		agent1.sources.source1.host = master
		agent1.sources.source1.port = 52020
		
		agent1.sources.source1.interceptors = interceptor1
		agent1.sources.source1.interceptors.interceptor1.type = org.apache.flume.sink.solr.morphline.UUIDInterceptor$Builder
		agent1.sources.source1.interceptors.interceptor1.headerName = key
		agent1.sources.source1.interceptors.interceptor1.preserveExisting = false
		
		# Describe the sink
		agent1.sinks.sink1.type = org.apache.flume.sink.kafka.KafkaSink
		agent1.sinks.sink1.brokerList  = master:9092
		agent1.sinks.sink1.topic = flume_kafka
		
		# Use a channel which buffers events in memory
		agent1.channels.channel1.type = memory
		agent1.channels.channel1.capacity = 1000
		agent1.channels.channel1.transactionCapacity = 100
		
		# Bind the source and sink to the channel
		agent1.sources.source1.channels = channel1
		agent1.sinks.sink1.channel = channel1


- 启动

	apache-flume-1.6.0-bin/目录下

		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_kafka_interceptor.properties --name agent1 -Dflume.root.logger=INFO,console

- 测试

		curl -X POST -d '[{"headers":{"flume":"flume is very easy!"}, "body":"111"}]' http://master:52020
		curl -X POST -d '[{"headers":{"areyouok":"NO", "flume":"flume is very easy!"}, "body":"I am not ok"}]' http://master:52020


	![flume_kafka_interceptor](https://img-blog.csdnimg.cn/20200517173729944.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)
