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

## 2.启动
apache-storm-0.9.3/conf/bin/目录下

- master

		python storm nimbus &
		python storm ui &
		python storm logviewer &

- slave1、slave2
	
		python storm supervisor &
		python storm logviewer &

## 3.停止

	kill -9 `ps aux | fgrep storm | fgrep -v 'fgrep' | awk '{print $2}'` 
