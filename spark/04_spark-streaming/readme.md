# 文件说明

- WordCount.scala 简单的wordCount
- WordCountWithState.scala 会记录历史的wordCount
- WindowTest.scala 只记录当前某时间段的wordCount

----

- KafkaReceiver.scala kafka的receive模式
- KafkaDirect.scala kafka的direct模式

----

- wc_local.sh wordCount本地模式
- wc_standalone.sh wordCount单机模式
- wc_cluster.sh wordCount集群模式

---

- wc_state.sh wordCount状态管理
- wc_window.sh wordCount窗口函数
- wc_kafka.sh wordCount与kafka连接


# 创建一个SparkStreaming

## 1、StreamingContext

	val ssc = new StreamingContext(sparkConf, Seconds(10))

- 是流计算功能的主要入口
- 会在底层创建SparkContext，用来处理数据
- 构造函数接受用来指定多长时间处理一次新数据的批次间隔(batch interval)，单位s

## 2、socketTextStream

	val lines = ssc.socketTextStream("localhost", 9999) 

创建出基于本地9999端口上收到的文本数据DStream

## 3、start()

- 只要设定好了要进行的计算，系统收到数据时就算就会开始
- 要开始接受数据，必须显示调用StreamingContext的start()方法。这样Spark Streaming就会开始把Spark作业不断交给下面的Spark Context去调度执行

## 4、awaitTermination()

执行会在另一个线程中进行，所以需要调用awaitTermination()来等待流计算完成，以防止应用退出

# 操作说明

## 1.运行任务

1>标准输出 2>错误输出

	bash wc_local.sh 1>1.log 2>2.log

## 2.监控日志

	tail -f 1.log

## 3.打开端口

	nc -l 9999


## 4.测试wordCount

### 4.1local

	/usr/local/src/spark-1.6.0-bin-hadoop2.6/bin/spark-submit \
		--master local[2] \
		--class com.albert.streaming.test.WordCount /usr/local/src/learn/albert/25_spark_streaming/streaming-1.0-SNAPSHOT.jar \
		master \
		9999

![测试wordCount](https://img-blog.csdnimg.cn/20200530190052382.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

### 4.2standalone

	/usr/local/src/spark-1.6.0-bin-hadoop2.6/bin/spark-submit \
		--master spark://master:7077 \
		--num-executors 2 \
		--executor-memory 1g \
		--executor-cores 2 \
		--driver-memory 1g \
		--class com.albert.streaming.test.WordCount /usr/local/src/learn/albert/25_spark_streaming/streaming-1.0-SNAPSHOT.jar \
		master \
		9999


![在这里插入图片描述](https://img-blog.csdnimg.cn/202006030608152.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

### 4.3cluster

	/usr/local/src/spark-1.6.0-bin-hadoop2.6/bin/spark-submit \
		--master yarn-cluster \
		--num-executors 2 \
		--executor-memory 1g \
		--executor-cores 2 \
		--driver-memory 1g \
		--class com.albert.streaming.test.WordCount /usr/local/src/learn/albert/25_spark_streaming/streaming-1.0-SNAPSHOT.jar \
		master \
		9999

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200603055937535.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

杀掉任务
	yarn application -kill application_1590989536331_0001

## 5.测试WordCountWithState

会保存历史的信息

## 6.测试windowTest

只保留某个时间点往前的信息，比如只保存5秒钟，9:00:00的时候，此时的数据是8:59:55-9:00:00这个时间段内的数据，9:00:30的时候，此时的数据是9:00:25-9:00:30这个时间段内的数据，


只测本地，其他测试同4

![windowTest](https://img-blog.csdnimg.cn/20200602181634185.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

## 7.测试kafka