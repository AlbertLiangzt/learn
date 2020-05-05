## 创建表
	> create 'm_table', 'meta_data', 'action'

## 查看所有表
	> list
	
## 查看表结构
	> desc 'm_table'

## 添加列簇
	> alter 'm_table', {NAME=>'cf_new', VERSIONS=>3, IN_MEMORY=>true}

## 删除列簇
	> alter 'm_table', {NAME=>'action', METHOD=>'delete'}

## hdfs查看对应的结构
	hadoop fs -ls /hbase/data/default/m_table/xxxx
	
xxx代表region，更多信息可以在浏览器上查看

http://master:60010/table.jsp?name=m_table

## 删除表：
	> disable 'm_table'
	> drop 'm_table'

先将状态设为不可用，再删除，删除后hdfs没有数据

## 写数据：
	> put 'm_table', '1001', 'meta_data:name', 'zhang3'
	> put 'm_table', '1001', 'meta_data:age', '18'
	> put 'm_table', '1002', 'meta_data:name', 'li4'
	> put 'm_table', '1002', 'meta_data:gender', 'man'

若想此时在hdfs上进行查看，需
	> flush 'm_table'

## 读数据：
### 全表扫描
	> scan "m_table"
### 读一条记录：
	> get "m_table", '1001'