1.安装mysql

2.解压缩

	tar -zxvf apache-hive-1.2.2-bin.tar.gz

3.hive/lib增加文件

	mysql-connector-java-5.1.41-bin.jar

4.hive/conf增加文件

	hive-site.xml

5.配置hadoop_home目录

	cp hive-env.sh.template hive-env.sh
	vim hive-env.sh
	新增
	HADOOP_HOME=/usr/local/src/hadoop-2.6.5

6.删除冲突jar包(具体jar名与版本有关)

	rm -f /usr/local/src/hadoop-2.6.5/share/hadoop/yarn/lib/jline-0.9.94.jar
	cp /usr/local/src/apache-hive-1.2.2-bin/lib/jline-2.12.jar /usr/local/src/hadoop-2.6.5/share/hadoop/yarn/lib/
不然启动会报错<font color=red size=5>java.lang.IncompatibleClassChangeError: Found class jline.Terminal, but interface was expected</font>
![jar包冲突](https://img-blog.csdnimg.cn/20200424215351920.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

7.配置环境变量，修改bashrc

	vim ~/.bashrc
	新增
	export HIVE_HOME=/usr/local/src/apache-hive-1.2.2-bin
	export PATH=$PATH:$HIVE_HOME/bin

8.重启配置

	source ~/.bashrc

7.启动hive

注意，启动hive时，hadoop必须先启动
	hive
![start hive](https://img-blog.csdnimg.cn/20200424220354431.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)


