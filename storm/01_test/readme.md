## 文件说明
- WordCount.java	wordCount主程序
- WordCountSpout.java	spout
- SplitSentence.java	模拟第一个bolt部分数据失败
- WordCountBolt.java	bolt
- pom.xml	配置文件
- run.sh	启动脚本

注意，打成包含依赖jar包的jar包时，删除storm-core.jar——storm-core下面也存在一个defaults.yaml文件，因此storm运行时报错冲突

## 0.解压缩

	tar -zxvf apache-storm-0.9.3.tar.gz

## 1.修改配置文件

apache-storm-0.9.3/conf/目录下

storm.yaml新增参数

	storm.zookeeper.servers:
		- "master"
		- "slave1"
		- "slave2"
	
	ui.port: 6705
	nimbus.host: "master"
	supervisor.slots.ports:
		- 6700
		- 6701
		- 6702
		- 6703
		- 6704
	
ui.port参数，是storm的ui页面。如果不设置，默认为8080端口，与spark冲突

## 2.启动服务
apache-storm-0.9.3/conf/bin/目录下

- master

		python storm nimbus &
		python storm ui &
		python storm logviewer &

- slave1、slave2
	
		python storm supervisor &
		python storm logviewer &

## 3.停止服务

	kill -9 `ps aux | fgrep storm | fgrep -v 'fgrep' | awk '{print $2}'` 

## 4.启动任务

### 4.1启动本地任务
	python /usr/local/src/apache-storm-0.9.3/bin/storm jar \
		/usr/local/src/learn/albert/23_storm/01_test.jar \
		WordCount \
		local
### 4.2启动集群任务
	python /usr/local/src/apache-storm-0.9.3/bin/storm jar \
		/usr/local/src/learn/albert/23_storm/01_test.jar \
		WordCount \
		remote

## 5.结束任务
### 5.1结束本地任务

CTRL+C

### 5.2结束集群任务

UI页面进行kill

![kill](https://img-blog.csdnimg.cn/20200524154730539.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)