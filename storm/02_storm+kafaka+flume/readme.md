## 文件说明

- flume_kafka_storm.properties	flume配置
- storm_master_lib.zip	storm在master节点的lib包
- storm_slave_lib.zip	storm在slave节点的lib包
- StormKafka.java	StormKafka的测试类
- PrinterBolt.java	只做输出
- run_storm_kafka.sh	启动脚本

# <font color=red>一、kafka+storm</font>

## 0.放入依赖的jar包

可以直接下载使用，注意StormKafka.java、flume_kafka_storm.properties中的topic名称

### 0.1 storm-kafka相关

需要将storm-kafka-0.9.3.jar放到storm里
	/usr/local/src/apache-storm-0.9.3/lib/

不然启动storm会报错

	Error: A JNI error has occurred, please check your installation and try again
	Exception in thread "main" java.lang.NoClassDefFoundError: storm/kafka/BrokerHosts
		at java.lang.Class.getDeclaredMethods0(Native Method)
		at java.lang.Class.privateGetDeclaredMethods(Class.java:2701)
		at java.lang.Class.privateGetMethodRecursive(Class.java:3048)
		at java.lang.Class.getMethod0(Class.java:3018)
		at java.lang.Class.getMethod(Class.java:1784)
		at sun.launcher.LauncherHelper.validateMainClass(LauncherHelper.java:544)
		at sun.launcher.LauncherHelper.checkAndLoadMain(LauncherHelper.java:526)
	Caused by: java.lang.ClassNotFoundException: storm.kafka.BrokerHosts
		at java.net.URLClassLoader.findClass(URLClassLoader.java:381)
		at java.lang.ClassLoader.loadClass(ClassLoader.java:424)
		at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:349)
		at java.lang.ClassLoader.loadClass(ClassLoader.java:357)
		... 7 more

## 0.2 kafka相关
	
需要将kafka_2.11-0.10.2.1.jar、kafka-clients-0.10.2.1.jar放到storm里
	/usr/local/src/apache-storm-0.9.3/lib/

缺kafka_2.11-0.10.2.1.jar报错

	Exception in thread "main" java.lang.NoClassDefFoundError: kafka/api/OffsetRequest
		at storm.kafka.KafkaConfig.<init>(KafkaConfig.java:43)
		at storm.kafka.SpoutConfig.<init>(SpoutConfig.java:32)
		at stormKafka.StormKafka.main(StormKafka.java:17)
	Caused by: java.lang.ClassNotFoundException: kafka.api.OffsetRequest
		at java.net.URLClassLoader.findClass(URLClassLoader.java:381)
		at java.lang.ClassLoader.loadClass(ClassLoader.java:424)
		at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:349)
		at java.lang.ClassLoader.loadClass(ClassLoader.java:357)
		... 3 more

缺kafka-clients-0.10.2.1.jar报错

	Exception in thread "main" java.lang.NoClassDefFoundError: org/apache/kafka/common/network/Send
		at storm.kafka.KafkaConfig.<init>(KafkaConfig.java:43)
		at storm.kafka.SpoutConfig.<init>(SpoutConfig.java:32)
		at stormKafka.StormKafka.main(StormKafka.java:17)
	Caused by: java.lang.ClassNotFoundException: org.apache.kafka.common.network.Send
		at java.net.URLClassLoader.findClass(URLClassLoader.java:381)
		at java.lang.ClassLoader.loadClass(ClassLoader.java:424)
		at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:349)
		at java.lang.ClassLoader.loadClass(ClassLoader.java:357)
		... 3 more


<font color=red>注意:这两个jar包版本必须匹配，具体包可以在/usr/local/src/kafka_2.11-0.10.2.1/libs找到</font>

包不匹配则报错

	ERROR backtype.storm.util - Async loop died!
	java.lang.NoSuchMethodError: scala.Predef$.ArrowAssoc(Ljava/lang/Object;)Ljava/lang/Object;
		at kafka.consumer.FetchRequestAndResponseMetrics.<init>(FetchRequestAndResponseStats.scala:32) ~[kafka_2.11-0.9.0.0.jar:na]
		at kafka.consumer.FetchRequestAndResponseStats.<init>(FetchRequestAndResponseStats.scala:47) ~[kafka_2.11-0.9.0.0.jar:na]
		at kafka.consumer.FetchRequestAndResponseStatsRegistry$$anonfun$2.apply(FetchRequestAndResponseStats.scala:60) ~[kafka_2.11-0.9.0.0.jar:na]
		at kafka.consumer.FetchRequestAndResponseStatsRegistry$$anonfun$2.apply(FetchRequestAndResponseStats.scala:60) ~[kafka_2.11-0.9.0.0.jar:na]
		at kafka.utils.Pool.getAndMaybePut(Pool.scala:61) ~[kafka_2.11-0.9.0.0.jar:na]
		at kafka.consumer.FetchRequestAndResponseStatsRegistry$.getFetchRequestAndResponseStats(FetchRequestAndResponseStats.scala:64) ~[kafka_2.11-0.9.0.0.jar:na]
		at kafka.consumer.SimpleConsumer.<init>(SimpleConsumer.scala:44) ~[kafka_2.11-0.9.0.0.jar:na]
		at kafka.javaapi.consumer.SimpleConsumer.<init>(SimpleConsumer.scala:34) ~[kafka_2.11-0.9.0.0.jar:na]
		at storm.kafka.DynamicPartitionConnections.register(DynamicPartitionConnections.java:60) ~[storm-kafka-0.9.3.jar:0.9.3]
		at storm.kafka.PartitionManager.<init>(PartitionManager.java:64) ~[storm-kafka-0.9.3.jar:0.9.3]
		at storm.kafka.ZkCoordinator.refresh(ZkCoordinator.java:98) ~[storm-kafka-0.9.3.jar:0.9.3]
		at storm.kafka.ZkCoordinator.getMyManagedPartitions(ZkCoordinator.java:69) ~[storm-kafka-0.9.3.jar:0.9.3]
		at storm.kafka.KafkaSpout.nextTuple(KafkaSpout.java:135) ~[storm-kafka-0.9.3.jar:0.9.3]
		at backtype.storm.daemon.executor$fn__3373$fn__3388$fn__3417.invoke(executor.clj:565) ~[storm-core-0.9.3.jar:0.9.3]
		at backtype.storm.util$async_loop$fn__464.invoke(util.clj:463) ~[storm-core-0.9.3.jar:0.9.3]
		at clojure.lang.AFn.run(AFn.java:24) [clojure-1.5.1.jar:na]
		at java.lang.Thread.run(Thread.java:748) [na:1.8.0_172]

### curator-client-2.4.0.jar

	ERROR backtype.storm.util - Async loop died!
	java.lang.NoClassDefFoundError: org/apache/curator/RetryPolicy
		at storm.kafka.KafkaSpout.open(KafkaSpout.java:85) ~[storm-kafka-0.9.3.jar:0.9.3]
		at backtype.storm.daemon.executor$fn__3373$fn__3388.invoke(executor.clj:522) ~[storm-core-0.9.3.jar:0.9.3]
		at backtype.storm.util$async_loop$fn__464.invoke(util.clj:461) ~[storm-core-0.9.3.jar:0.9.3]
		at clojure.lang.AFn.run(AFn.java:24) [clojure-1.5.1.jar:na]
		at java.lang.Thread.run(Thread.java:748) [na:1.8.0_172]
	Caused by: java.lang.ClassNotFoundException: org.apache.curator.RetryPolicy
		at java.net.URLClassLoader.findClass(URLClassLoader.java:381) ~[na:1.8.0_172]
		at java.lang.ClassLoader.loadClass(ClassLoader.java:424) ~[na:1.8.0_172]
		at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:349) ~[na:1.8.0_172]
		at java.lang.ClassLoader.loadClass(ClassLoader.java:357) ~[na:1.8.0_172]
		... 5 common frames omitted


### curator-framework-2.4.0.jar

	ERROR backtype.storm.util - Async loop died!
	java.lang.NoClassDefFoundError: org/apache/curator/framework/CuratorFrameworkFactory
		at storm.kafka.ZkState.newCurator(ZkState.java:45) ~[storm-kafka-0.9.3.jar:0.9.3]
		at storm.kafka.ZkState.<init>(ZkState.java:61) ~[storm-kafka-0.9.3.jar:0.9.3]
		at storm.kafka.KafkaSpout.open(KafkaSpout.java:85) ~[storm-kafka-0.9.3.jar:0.9.3]
		at backtype.storm.daemon.executor$fn__3373$fn__3388.invoke(executor.clj:522) ~[storm-core-0.9.3.jar:0.9.3]
		at backtype.storm.util$async_loop$fn__464.invoke(util.clj:461) ~[storm-core-0.9.3.jar:0.9.3]
		at clojure.lang.AFn.run(AFn.java:24) [clojure-1.5.1.jar:na]
		at java.lang.Thread.run(Thread.java:748) [na:1.8.0_172]


## 2.启动服务
### 2.1 启动storm
apache-storm-0.9.3/conf/bin/目录下

- master

		python storm nimbus &
		python storm ui &
		python storm logviewer &

- slave1、slave2
	
		python storm supervisor &
		python storm logviewer &

### 2.2 启动kafka
kafka_2.11-0.10.2.1/目录下

- master、slave1、slave2

		./bin/kafka-server-start.sh ./config/server.properties &

## 3.启动任务

### 3.1启动kafka producer
kafka_2.11-0.10.2.1/目录下

	./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic storm_kafka

### 3.2启动storm任务
与kafka+storm的storm任务一样

	python /usr/local/src/apache-storm-0.9.3/bin/storm jar \
	    /usr/local/src/learn/albert/24_storm_extend/extend.jar \
	    stormKafka.StormKafka \


![start](https://img-blog.csdnimg.cn/20200605113412442.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)


# <font color=red>二、flume+kafka+storm</font>

在kafka+storm、flume+kafka的基础上，就能实现flume+kafka+storm

## 1.启动服务
## 1.1启动flume

	./bin/flume-ng agent --conf conf --conf-file ./conf/flume_kafka_storm.properties --name agent1 -Dflume.root.logger=INFO,console

### 1.2启动kafka
kafka_2.11-0.10.2.1/目录下

- master、slave1、slave2

		./bin/kafka-server-start.sh ./config/server.properties &

### 1.3启动storm

apache-storm-0.9.3/conf/bin/目录下

- master

		python storm nimbus &
		python storm ui &
		python storm logviewer &

- slave1、slave2
	
		python storm supervisor &
		python storm logviewer &

## 2.启动任务

### 2.1启动storm任务

	python /usr/local/src/apache-storm-0.9.3/bin/storm jar \
	    /usr/local/src/learn/albert/24_storm_extend/extend.jar \
	    stormKafka.StormKafka \

### 2.2flume端进行输出

由flume_kafka_storm.properties配置

apache-flume-1.6.0-bin/目录下

  	./bin/flume-ng agent --conf conf --conf-file ./conf/flume_kafka_storm.properties --name agent1 -Dflume.root.logger=INFO,console

![flume kafka storm](https://img-blog.csdnimg.cn/20200606223955614.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)


# 附：停止storm进程
master、slave1、slave2下执行

	kill -9 `ps aux | fgrep storm | fgrep -v 'fgrep' | awk '{print $2}'` 


# 附：<a href="https://blog.csdn.net/AlbertLiangzt/article/details/106178294">flume+kafka测试</a>
