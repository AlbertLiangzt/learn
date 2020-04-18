## 一、安装

### 1.解压缩spark-1.6.0-bin-hadoop2.6.tgz

	tar -zxvf spark-1.6.0-bin-hadoop2.6.tgz

### 2.进入con目录

- spark-env.sh新增参数
	
	`cp spark-env.sh.template spark-env.sh`

	`vim spark-env.sh`

		export SCALA_HOME=/usr/local/src/scala-2.10.5
		export JAVA_HOME=/usr/local/src/jdk1.8.0_172
		export HADOOP_HOME=/usr/local/src/hadoop-2.6.5
		export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
		SPARK_MASTER_IP=master
		SPARK_LOCAL_DIRS=/usr/local/src/spark-1.6.0-bin-hadoop2.6
		SPARK_DRIVER_MEMORY=1G

	![在这里插入图片描述](https://img-blog.csdnimg.cn/20200411221633211.png)


- slaves新增参数

	`cp slaves.template slaves`

	`vim slaves`

		slave1		#从节点的hostname或者ip
		slave2

	![在这里插入图片描述](https://img-blog.csdnimg.cn/20200411221646912.png)

### 3.将spark-1.6.0-bin-hadoop2.6分发到slave、slave2

	scp -r spark-1.6.0-bin-hadoop2.6 slave1:/usr/local/src
	scp -r spark-1.6.0-bin-hadoop2.6 slave2:/usr/local/src

### 4.启动Spark

	./sbin/start-all.sh

启动成功标志

- master会有Master进程

- slave会有Worker进程

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200411221053428.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

## 二、验证

### 1.本地模式：

终端展示运行结果

	 ./bin/run-example SparkPi 10 --master local[2]

### 2.集群模式 Spark Standalone：
	
从spark监控页面看结果
	
终端展示运行结果

	./bin/spark-submit   --class org.apache.spark.examples.SparkPi --master spark://master:7077 lib/spark-examples-1.6.0-hadoop2.6.0.jar   100

### 3.集群模式 Spark on Yarn集群上yarn-cluster模式：
	
从yarn集群看结果

yarn集群log运行结果

	./bin/spark-submit --class org.apache.spark.examples.SparkPi --master yarn-cluster lib/spark-examples-1.6.0-hadoop2.6.0.jar 10
