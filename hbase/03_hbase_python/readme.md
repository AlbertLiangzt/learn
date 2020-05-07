# 文件说明
- hbase	hbase模块
- thrift thrift模块
- 1_create_table.py 创建表
- 2_insert_data.py 插入数据
- 3_get_data.py 获取数据
- 4_scan_table.py 扫描表

# 安装thrift
- 1.解压缩tar包

	tar -zxvf thrift-0.8.0.tar.gz

- 2.安装

	thrift/目录下执行

		./configure
		make
		make install

- 3.启动服务
	
	hbase/bin目录下执行

		./hbase-daemon.sh start thrift

- 4.添加thrift模块

	将thrift模块文件夹移到项目中

	开发python代码，通过thrift协议将数据进行传输

		cp -r /usr/local/src/thrift-0.8.0/lib/py/build/lib.linux-x86_64-2.7/thrift/ /usr/local/src/learn/albert/19_hbase_python/
- 5.添加hbase模块
	- 5.1 解压hbase源码包
	
		<font color=red>注意：源码包需要与hbase版本匹配</font>
	
			tar -zxvf hbase-0.98.24-src.tar.gz

	- 5.2 生成python hbase模块
	
		hbase-0.98.24/hbase-thrift/src/main/resources/org/apache/hadoop/hbase/thrift目录下执行
			
			thrift --gen py Hbase.thrift

	- 5.3 添加hbase模块
			
		上一步5.2生成的gen-py/hbase文件夹移到项目中	

			cp -r /usr/local/src/hbase-0.98.24/hbase-thrift/src/main/resources/org/apache/hadoop/hbase/thrift/gen-py/hbase/ /usr/local/src/learn/albert/19_hbase_python/
