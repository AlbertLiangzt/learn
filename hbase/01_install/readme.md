## 0.前提zookeeper

## 1.解压缩
	
	tar -zxvf hbase-0.98.6-hadoop2-bin.tar.gz

## 2.配置环境

hbase/conf目录下

- hbase-env.sh

		vim hbase-env.sh
		# 新增
		export JAVA_HOME=/usr/local/src/jdk1.8.0_172
		export HBASE_MANAGES_ZK=false # false用第三方zk

- hbase-site.xml

		vim hbase-site.xml
		# 新增
		<configuration>
			<!-- 数据存储路径 -->
			<property>
				<name>hbase.rootdir</name>
				<value>hdfs://master:9000/hbase</value>
			</property>
			<!-- 是否分布式 -->
			<property>
				<name>hbase.cluster.distributed</name>
				<value>true</value>
			</property>
			<!-- zk地址 -->
		    <property>
				<name>hbase.zookeeper.quorum</name>
				<value>master,slave1,slave2</value>
			</property>
			<!-- 与master节点时间差 ms -->
			<property>
				<name>hbase.master.maxclockskew</name>
				<value>150000</value>
			</property>
			<!-- hdfs需要的复本数 -->
		    <!--<property>-->
		         <!--<name>dfs.replication</name>-->
		         <!--<value>2</value>-->
	     <!--</property>-->
		</configuration>

- regionservers

		vim regionservers
		修改为
		slave1
		slave2


## 3.分发到从节点

	scp -r hbase-0.98.6-hadoop2 slave1:/usr/local/src/
	scp -r hbase-0.98.6-hadoop2 slave2:/usr/local/src/

## 4.启动

hbase/bin目录下

	./start-hbase.sh

## 5.检查服务情况

- 浏览器查看

		http://master:60010/master-status
	![browser](https://img-blog.csdnimg.cn/20200430223516860.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

- hive查看
	
		# hbase/bin目录下
		./hbase shell
		hbase> status

	![shell](https://img-blog.csdnimg.cn/2020043022361085.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

- 进程查看

	- master会有HMaster进程

	- slave会有HRegionServer进程
	
	![在这里插入图片描述](https://img-blog.csdnimg.cn/20200513214457754.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)