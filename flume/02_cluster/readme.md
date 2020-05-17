## 文件说明
#### sink组

- master

	- flume_1_1_failover.properties 故障转移
	- flume_1_2_loadbalance.properties 负载均衡

- slave

	- flume_server.properties

#### 拦截与过滤interceptor

- flume_2_1_timestamp.properties	时间戳
- flume_2_2_host.properties	hostname
- flume_2_3_static.properties	static
- flume_2_4_regex_filter.properties	regex filter
- flume_2_5_regex_extractor.properties	regex extractor

#### 复制与复用
- master
	- flume_3_1_replicating.properties 复制
	- flume_3_2_multiplexing.properties	复用
- slave
	- flume_server_select_slave1.properties slave1
	- flume_server_select_slave2.properties	slave2

# 1.sink组

## 1.1 故障转移（failover）

### 1.1.1配置 flume/conf/目录下

- master
			
	新建flume_1_1_failover.properties，并添加下列参数

		# Name the components on this agent
		agent1.sources = source1
		agent1.sinks = sink1 sink2
		agent1.channels = channel1
		agent1.sinkgroups = sinkgroup1
	
		# Describe/configure the source
		agent1.sources.source1.channels = channel1
		agent1.sources.source1.type = exec
		agent1.sources.source1.command = tail -F /usr/local/src/learn/albert/21_flume/2.log

		# Describe the sink
		agent1.sinks.sink1.channel = channel1
		agent1.sinks.sink1.type = avro
		agent1.sinks.sink1.hostname = slave1
		agent1.sinks.sink1.port = 52020
	
		agent1.sinks.sink2.channel = channel1
		agent1.sinks.sink2.type = avro
		agent1.sinks.sink2.hostname = slave2
		agent1.sinks.sink2.port = 52020

		# Use a channel which buffers events in memory
		agent1.channels.channel1.type = memory
		agent1.channels.channel1.capacity = 1000
		agent1.channels.channel1.transactionCapacity = 100
	
		agent1.sinkgroups.sinkgroup1.sinks = sink1 sink2
		# set failover
		agent1.sinkgroups.sinkgroup1.processor.type = failover
		## priority
		agent1.sinkgroups.sinkgroup1.processor.sink1 = 10
		agent1.sinkgroups.sinkgroup1.processor.sink2 = 1
		agent1.sinkgroups.sinkgroup1.processor.maxpenalty = 10000

- slave1、slave2
		
	新建flume_server.properties，并添加下列参数
		
	注意：<font color=red>agent1.sources.source1.bind</font>的值，取决于服务器

		# agent1 name
		agent1.sources = source1
		agent1.sinks = sink1
		agent1.channels = channel1
		
		# set channel
		agent1.channels.channel1.type = memory
		agent1.channels.channel1.capacity = 1000
		agent1.channels.channel1.transactionCapacity = 100
		
		# other node, slave to master
		agent1.sources.source1.type = avro
		## depend on slave1 slave2
		agent1.sources.source1.bind = slave2
		agent1.sources.source1.port = 52020
		agent1.sources.source1.channels = channel1
		
		# set sink to hdfs
		agent1.sinks.sink1.type = logger
		agent1.sinks.sink1.channel = channel1



### 1.1.2启动
	
先启动master会报错，忽略，直接启动slave即可
	
- master

		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_1_1_failover.properties --name agent1 -Dflume.root.logger=INFO,console
			
- slave1、slave2
		
		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_server.properties --name agent1 -Dflume.root.logger=INFO,console

		
### 1.1.3测试
		
master新建窗口

/usr/local/src/learn/albert/21_flume/目录下

<font color=red>根据优先级，会优先发送信息到指定服务器，当那台服务器挂掉CTRL+C，则会发送到另一台服务器</font>
		
![1-1](https://img-blog.csdnimg.cn/20200512235940552.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

## 1.2 负载均衡（load_balance）

### 1.2.1配置 flume/conf/目录下
	
- master
		
	新建flume_1_2_loadbalance.properties，并添加下列参数

		# Name the components on this agent
		agent1.sources = source1
		agent1.sinks = sink1 sink2
		agent1.channels = channel1
		agent1.sinkgroups = sinkgroup1
		
		# Describe/configure the source
		agent1.sources.source1.channels = channel1
		agent1.sources.source1.type = exec
		agent1.sources.source1.command = tail -F /usr/local/src/learn/albert/21_flume/2.log
		
		# Describe the sink
		agent1.sinks.sink1.channel = channel1
		agent1.sinks.sink1.type = avro
		agent1.sinks.sink1.hostname = slave1
		agent1.sinks.sink1.port = 52020
		
		agent1.sinks.sink2.channel = channel1
		agent1.sinks.sink2.type = avro
		agent1.sinks.sink2.hostname = slave2
		agent1.sinks.sink2.port = 52020
		
		# Use a channel which buffers events in memory
		agent1.channels.channel1.type = memory
		agent1.channels.channel1.capacity = 1000
		agent1.channels.channel1.transactionCapacity = 100
		
		agent1.sinkgroups.sinkgroup1.sinks = sink1 sink2
		agent1.sinkgroups.sinkgroup1.processor.type = load_balance
		agent1.sinkgroups.sinkgroup1.processor.selector = round_robin


- slave1、slave2
			
	同1.1参数相同

### 1.2.2启动
		
- master

		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_1_2_loadbalance.properties --name agent1 -Dflume.root.logger=INFO,console

- slave1、slave2(同1.1)
			
		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_server.properties --name agent1 -Dflume.root.logger=INFO,console
		
### 1.2.3测试

master新建窗口

/usr/local/src/learn/albert/21_flume/目录下

![1-2](https://img-blog.csdnimg.cn/20200512235952295.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

# 2.拦截与过滤interceptor


## 2.1 Timestamp

### 2.1.1配置 flume/conf/目录下
	
- master

	新建flume_2_1_timestamp.properties，并添加下列参数

		# agent1 name
		agent1.sources = source1
		agent1.sinks = sink1
		agent1.channels = channel1
		
		agent1.sources.source1.type = http
		agent1.sources.source1.host = master
		agent1.sources.source1.port = 52020
		agent1.sources.source1.channels = channel1
		
		agent1.sources.source1.interceptors = interceptor1
		agent1.sources.source1.interceptors.interceptor1.preserveExisting = false
		agent1.sources.source1.interceptors.interceptor1.type = timestamp
		
		agent1.sinks.sink1.type = hdfs
		agent1.sinks.sink1.channel = channel1
		agent1.sinks.sink1.hdfs.path =hdfs://master:9000/flume/%Y-%m-%d/%H%M
		agent1.sinks.sink1.hdfs.filePrefix = test_
		agent1.sinks.sink1.hdfs.fileType = DataStream
		agent1.sinks.sink1.channel = channel1
		
		agent1.channels.channel1.type = memory
		agent1.channels.channel1.capacity = 1000
		agent1.channels.channel1.transactionCapacity = 100
					

### 2.1.2启动
	
- master

		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_2_1_timestamp.properties --name agent1 -Dflume.root.logger=INFO,console

		
### 2.1.3测试
任意目录下

	curl -X POST -d '[{"headers":{"flume":"flume test"}, "body":"hello body"}]' http://master:52020

![Timestamp](https://img-blog.csdnimg.cn/20200513230422654.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

## 2.2 host

### 2.2.1配置 flume/conf/目录下
	
- master

	新建flume_2_2_host.properties，并添加下列参数

		# agent1 name
		agent1.sources = source1
		agent1.sinks = sink1
		agent1.channels = channel1
		
		agent1.sources.source1.type = syslogtcp
		agent1.sources.source1.host = master
		agent1.sources.source1.port = 52020
		agent1.sources.source1.channels = channel1
		
		agent1.sources.source1.interceptors = interceptor1 interceptor2
		agent1.sources.source1.interceptors.interceptor1.preserveExisting = false  
		agent1.sources.source1.interceptors.interceptor1.type = timestamp  
		agent1.sources.source1.interceptors.interceptor2.type = host  
		agent1.sources.source1.interceptors.interceptor2.hostHeader = hostname  
		agent1.sources.source1.interceptors.interceptor2.useIP = false  
		
		agent1.sinks.sink1.type = hdfs
		agent1.sinks.sink1.channel = channel1
		agent1.sinks.sink1.hdfs.path = hdfs://master:9000/flume/%Y-%m-%d/%H%M  
		agent1.sinks.sink1.hdfs.filePrefix = %{hostname}.
		agent1.sinks.sink1.hdfs.fileType = DataStream
		
		agent1.channels.channel1.type = memory
		agent1.channels.channel1.capacity = 1000
		agent1.channels.channel1.transactionCapacity = 100
		
		agent1.sources.source1.channels = channel1
		agent1.sinks.sink1.channel = channel1


### 2.2.2启动
	
- master

		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_2_2_host.properties --name agent1 -Dflume.root.logger=INFO,console
	
### 2.2.3测试
任意目录下

	echo "abcabc123123" | nc master 52020

![host](https://img-blog.csdnimg.cn/20200513230517240.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)
			

## 2.3 static

### 2.3.1配置 flume/conf/目录下
	
- master

	新建flume_2_3_static.properties，并添加下列参数

		
		# agent1 name
		agent1.sources = source1
		agent1.sinks = sink1
		agent1.channels = channel1
		
		agent1.sources.source1.type = http
		agent1.sources.source1.host = master
		agent1.sources.source1.port = 52020
		agent1.sources.source1.channels = channel1
		
		agent1.sources.source1.interceptors = interceptor1  
		agent1.sources.source1.interceptors.interceptor1.type = static  
		agent1.sources.source1.interceptors.interceptor1.key = flume_test
		agent1.sources.source1.interceptors.interceptor1.value = so_easy
		
		agent1.sinks.sink1.type = logger
		agent1.sinks.sink1.channel = channel1
		
		agent1.channels.channel1.type = memory
		agent1.channels.channel1.capacity = 1000
		agent1.channels.channel1.transactionCapacity = 100


### 2.3.2启动
	
- master

		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_2_3_static.properties --name agent1 -Dflume.root.logger=INFO,console

		
### 2.3.3测试
任意目录下

	curl -X POST -d '[{"headers":{"flume":"flume test again"}, "body":"hello word again"}]' http://master:52020

![static](https://img-blog.csdnimg.cn/20200513230555120.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

## 2.4 regex filter

### 2.4.1配置 flume/conf/目录下
	
- master

	新建flume_2_4_regex_filter.properties，并添加下列参数

		# agent1 name
		agent1.sources = source1
		agent1.sinks = sink1
		agent1.channels = channel1
		
		agent1.sources.source1.type = http
		agent1.sources.source1.host = master
		agent1.sources.source1.port = 52020
		agent1.sources.source1.channels = channel1
		
		agent1.sources.source1.interceptors = interceptor1
		agent1.sources.source1.interceptors.interceptor1.type = regex_filter
		agent1.sources.source1.interceptors.interceptor1.regex = ^[0-9]*$
		agent1.sources.source1.interceptors.interceptor1.excludeEvents = true
		
		agent1.sinks.sink1.type = logger
		agent1.sinks.sink1.channel = channel1
		
		agent1.channels.channel1.type = memory
		agent1.channels.channel1.capacity = 1000
		agent1.channels.channel1.transactionCapacity = 100


### 2.4.2启动
	
- master

		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_2_4_regex_filter.properties --name agent1 -Dflume.root.logger=INFO,console
		
### 2.4.3测试
任意目录下

	curl -X POST -d '[{"headers":{"flume":"flume is very easy!"}, "body":"111"}]' http://master:52020
	curl -X POST -d '[{"headers":{"flume":"flume is very easy!"}, "body":"test"}]' http://master:52020

![regex filter](https://img-blog.csdnimg.cn/20200513230624247.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

## 2.5 regex extractor

### 2.5.1配置 flume/conf/目录下
	
- master

	新建flume_2_5_regex_extractor.properties，并添加下列参数
				
		# agent1 name
		agent1.sources = source1
		agent1.sinks = sink1
		agent1.channels = channel1
		
		agent1.sources.source1.type = http
		agent1.sources.source1.host = master
		agent1.sources.source1.port = 52020
		agent1.sources.source1.channels = channel1
		
		agent1.sources.source1.interceptors = interceptor1
		agent1.sources.source1.interceptors.interceptor1.type = regex_extractor
		agent1.sources.source1.interceptors.interceptor1.regex = (\\d):(\\d):(\\d)
		agent1.sources.source1.interceptors.interceptor1.serializers = s1 s2 s3
		agent1.sources.source1.interceptors.interceptor1.serializers.s1.name = one
		agent1.sources.source1.interceptors.interceptor1.serializers.s2.name = two
		agent1.sources.source1.interceptors.interceptor1.serializers.s3.name = three
		
		agent1.sinks.sink1.type = logger
		agent1.sinks.sink1.channel = channel1
		
		agent1.channels.channel1.type = memory
		agent1.channels.channel1.capacity = 1000
		agent1.channels.channel1.transactionCapacity = 100
				

### 2.5.2启动
	
- master
		
		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_2_5_regex_extractor.properties --name agent1 -Dflume.root.logger=INFO,console

			
		
### 2.5.3测试
任意目录下

	curl -X POST -d '[{"headers":{"flume":"flume is very easy!"}, "body":"1:22:3:44ddd"}]' http://master:52020
	curl -X POST -d '[{"headers":{"flume":"flume is very easy!"}, "body":"1:2:a"}]' http://master:52020
	curl -X POST -d '[{"headers":{"flume":"flume is very easy!"}, "body":"1:2:3:4ddd"}]' http://master:52020


![regex extractor](https://img-blog.csdnimg.cn/20200513230649881.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

# 3.复制与复用（选择器selector）

## 3.1 复制replicating

### 3.1.1配置 flume/conf/目录下
	
- master
				
	新建flume_3_1_replicating.properties，并添加下列参数

		# Name the components on this agent  
		agent1.sources = source1
		agent1.sinks = sink1 sink2
		agent1.channels = channel1 channel2
		
		# Describe/configure the source
		agent1.sources.source1.type = syslogtcp
		agent1.sources.source1.port = 50000
		agent1.sources.source1.host = master
		agent1.sources.source1.selector.type = replicating
		agent1.sources.source1.channels = channel1 channel2
		
		# Describe the sink
		agent1.sinks.sink1.type = avro
		agent1.sinks.sink1.channel = channel1
		agent1.sinks.sink1.hostname = slave1
		agent1.sinks.sink1.port = 50000
		
		agent1.sinks.sink2.type = avro
		agent1.sinks.sink2.channel = channel2
		agent1.sinks.sink2.hostname = slave2
		agent1.sinks.sink2.port = 50000
		
		# Use a channel which buffers events inmemory
		agent1.channels.channel1.type = memory
		agent1.channels.channel1.capacity = 1000
		agent1.channels.channel1.transactionCapacity = 100
		
		agent1.channels.channel2.type = memory
		agent1.channels.channel2.capacity = 1000
		agent1.channels.channel2.transactionCapacity = 100


- slave1

	新建flume_server_select_slave1.properties，并添加下列参数

		# Name the components on this agent  
		agent1.sources = source1
		agent1.sinks = sink1
		agent1.channels = channel1
		   
		# Describe/configure the source
		agent1.sources.source1.type = avro
		agent1.sources.source1.channels = channel1
		agent1.sources.source1.bind = slave1
		agent1.sources.source1.port = 50000
		   
		# Describe the sink
		agent1.sinks.sink1.type = logger
		agent1.sinks.sink1.channel = channel1
		   
		# Use a channel which buffers events inmemory
		agent1.channels.channel1.type = memory
		agent1.channels.channel1.capacity = 1000
		agent1.channels.channel1.transactionCapacity = 100


- slave2
			
	新建flume_server_select_slave2.properties，并添加下列参数

		# Name the components on this agent  
		agent2.sources = source1
		agent2.sinks = sink1
		agent2.channels = channel1
		   
		# Describe/configure the source
		agent2.sources.source1.type = avro
		agent2.sources.source1.channels = channel1
		agent2.sources.source1.bind = slave2
		agent2.sources.source1.port = 50000
		   
		# Describe the sink
		agent2.sinks.sink1.type = logger
		agent2.sinks.sink1.channel = channel1
		   
		# Use a channel which buffers events inmemory
		agent2.channels.channel1.type = memory
		agent2.channels.channel1.capacity = 1000
		agent2.channels.channel1.transactionCapacity = 100
 
			

### 3.1.2启动
	
- master

		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_3_1_replicating.properties --name agent1 -Dflume.root.logger=INFO,console


- slave1

		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_server_select_slave2 --name agent1 -Dflume.root.logger=INFO,console

- slave2
		
		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_server_select_slave2 --name agent2 -Dflume.root.logger=INFO,console

		
### 3.1.3测试
任意目录下

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200514001127937.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)


## 3.2 复用multiplexing

### 3.2.1配置 flume/conf/目录下
	
- master
		
	新建flume_3_2_multiplexing.properties，并添加下列参数
		
		# Name the components on this agent  
		agent1.sources = source1
		agent1.sinks = sink1 sink2
		agent1.channels = channel1 channel2
		   
		# Describe/configure the source  
		agent1.sources.source1.type = org.apache.flume.source.http.HTTPSource
		agent1.sources.source1.port = 50000
		agent1.sources.source1.host = master
		agent1.sources.source1.selector.type = multiplexing
		agent1.sources.source1.channels = channel1 channel2
		
		agent1.sources.source1.selector.header = areyouok
		agent1.sources.source1.selector.mapping.OK = channel1
		agent1.sources.source1.selector.mapping.NO = channel2
		agent1.sources.source1.selector.default = channel1
		
		# Describe the sink
		agent1.sinks.sink1.type = avro
		agent1.sinks.sink1.channel = channel1
		agent1.sinks.sink1.hostname = slave1
		agent1.sinks.sink1.port = 50000
		       
		agent1.sinks.sink2.type = avro
		agent1.sinks.sink2.channel = channel2
		agent1.sinks.sink2.hostname = slave2
		agent1.sinks.sink2.port = 50000
		
		# Use a channel which buffers events inmemory  
		agent1.channels.channel1.type = memory
		agent1.channels.channel1.capacity = 1000
		agent1.channels.channel1.transactionCapacity = 100
				          
		agent1.channels.channel2.type = memory
		agent1.channels.channel2.capacity = 1000
		agent1.channels.channel2.transactionCapacity = 100


- slave1、slave2
			
	- slave1同3.1.1 slave1
	- slave2同3.1.1 slave2

### 3.2.2启动
	
- master

		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_3_2_multiplexing.properties --name agent1 -Dflume.root.logger=INFO,console


- slave1(同3.1.2 slave1)

		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_server_select_slave2 --name agent1 -Dflume.root.logger=INFO,console

- slave2(同3.1.2 slave2)
		
		./bin/flume-ng agent --conf conf --conf-file ./conf/flume_server_select_slave2 --name agent2 -Dflume.root.logger=INFO,console
		
### 3.3.3测试
任意目录下

	curl -X POST -d '[{"headers":{"areyouok":"OK", "flume":"flume is very easy!"}, "body":"I am ok"}]' http://master:50000
	curl -X POST -d '[{"headers":{"areyouok":"NO", "flume":"flume is very easy!"}, "body":"I am not ok"}]' http://master:50000
	curl -X POST -d '[{"headers":{"areyouok":"MAYBE", "flume":"flume is very easy!"}, "body":"I do not know"}]' http://master:52020
			
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200514001141370.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)