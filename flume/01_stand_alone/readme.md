## 1.解压缩

	tar -zxvf apache-flume-1.6.0-bin.tar.gz

## 2.单机模式

- 2.1 Netcat方式

	- 配置	flume/conf目录下
	
			# 新建配置文件
			touch flume_netcat.conf
			# 修改配置文件
			vim flume_netcat.conf
			# 新增
			agent1.sources = soureces1
			agent1.channels = channel1
			agent1.sinks = sinks1
	
			agent1.sources.soureces1.type = netcat
			agent1.sources.soureces1.bind = master
			agent1.sources.soureces1.port = 44444
	
			agent1.sinks.sinks1.type = logger
	
			agent1.channels.channel1.type = memory
			agent1.channels.channel1.capacity = 1000
			agent1.channels.channel1.transactionCapacity = 100
	
			agent1.sources.soureces1.channels = channel1
			agent1.sinks.sinks1.channel = channel1

	- 启动 flume/目录下

			./bin/flume-ng agent --conf conf --conf-file ./conf/flume_netcat.conf --name agent1 -Dflume.root.logger=INFO,console

	- 测试
	
		新开个窗口

			telnet master 44444


		![netcat](https://img-blog.csdnimg.cn/20200509142104642.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

- 2.2 exec方式
	- 配置 flume/conf目录下
		
			# 新建配置文件
			touch flume_exec.conf
			# 修改配置文件
			vim flume_exec.conf
			# 新增
			agent1.sources = soureces1
			agent1.channels = channel1
			agent1.sinks = sinks1
			
			agent1.sources.soureces1.type = exec
			agent1.sources.soureces1.command = tail -f /usr/local/src/learn/albert/21_flume/1.log
			
			agent1.sinks.sinks1.type = logger
			
			agent1.channels.channel1.type = memory
			agent1.channels.channel1.capacity = 1000
			agent1.channels.channel1.transactionCapacity = 100
			
			agent1.sources.soureces1.channels = channel1
			agent1.sinks.sinks1.channel = channel1

	- 启动 flume/目录下

			./bin/flume-ng agent --conf conf --conf-file ./conf/flume_exec.conf --name agent1 -Dflume.root.logger=INFO,console

	- 测试
	
		新开个窗口
			
		![exec](https://img-blog.csdnimg.cn/20200509143949380.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

- 2.3 hdfs方式

	- 配置 flume/conf目录下

			# 新建配置文件
			touch flume.conf
			# 修改配置文件
			vim flume.conf

	- flume.conf
	
			# Name the components on this agent
			agent1.sources = soureces1
			agent1.channels = channel1
			agent1.sinks = sinks1
			
			# Describe/configure the source
			agent1.sources.soureces1.type = exec
			agent1.sources.soureces1.command = tail -f /usr/local/src/learn/albert/21_flume/2.log
			
			# Describe the sink
			# 表示下沉到hdfs，类型决定了下面的参数
			agent1.sinks.skins1.type = hdfs
			agent1.sinks.skins1.channel = channel1
			## hdfs去写文件的位置
			agent1.sinks.skins1.hdfs.path = /flume/tailout/%y-%m-%d/%H%M/
			## 最后的文件的前缀
			agent1.sinks.skins1.hdfs.filePrefix = events-
			## 到触发的时间时，是否要更新文件夹
			agent1.sinks.skins1.hdfs.round = true
			## 表示每隔1分钟改变一次
			agent1.sinks.skins1.hdfs.roundValue = 1
			## 切换文件的时候的时间单位是分钟
			agent1.sinks.skins1.hdfs.roundUnit = minute
			## 表示只要过了3秒钟，就切换生成一个新的文件
			agent1.sinks.skins1.hdfs.rollInterval = 3
			## 如果记录的文件大于20字节时切换一次
			agent1.sinks.skins1.hdfs.rollSize = 20
			## 当写了5个事件时触发
			agent1.sinks.skins1.hdfs.rollCount = 5
			## 收到了多少条消息往hdfs中追加内容
			agent1.sinks.skins1.hdfs.batchSize = 10
			## 使用本地时间戳
			agent1.sinks.skins1.hdfs.useLocalTimeStamp = true
			#生成的文件类型，默认是Sequencefile，可用DataStream：为普通文本
			agent1.sinks.skins1.hdfs.fileType = DataStream
			
			# Use a channel which buffers events in memory
			agent1.channels.channel1.type = memory
			agent1.channels.channel1.capacity = 1000
			agent1.channels.channel1.transactionCapacity = 100
			
			# Bind the source and sink to the channel
			agent1.sources.soureces1.channels = channel1
			agent1.sinks.sinks1.channel = channel1

	- 启动
	
			./bin/flume-ng agent --conf conf --conf-file ./conf/flume.conf --name agent1 -Dflume.root.logger=INFO,console	
	![hdfs](https://img-blog.csdnimg.cn/20200511003119295.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)


# 附
## 1.telnet安装命令

未安装telnet

`rpm -qa telnet-server` 无结果

执行

	yum install telnet-server
	yum install telnet

## 2.退出Telnet

	CTRL+]
	quit