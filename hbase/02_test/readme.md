# 一、操作表结构
- 1.创建表
	
		> create 'm_table', 'meta_data', 'action'

- 2.删除表：

		> disable 'm_table'
		> drop 'm_table'

- 3.添加列簇

		> alter 'm_table', {NAME=>'cf_new', VERSIONS=>3, IN_MEMORY=>true}

- 4.删除列簇
	
		> alter 'm_table', {NAME=>'action', METHOD=>'delete'}
	先将状态设为不可用，再删除，删除后hdfs没有数据


- 5.清空数据

		> truncate 'm_table'

	![在这里插入图片描述](https://img-blog.csdnimg.cn/20200506144902807.png)

	处理逻辑
	- 1.先将状态设为不可用
	- 2.删除表
	- 3.创建表
	
- 6.修改版本号
设定版本号，版本号为几 就是存储几个版本的数据

		> alter 'm_table', {NAME=>'meta_data', VERSIONS=>3}
	
# 二、查看表信息
- 1.查看所有表
	
		> list
	
- 2.查看表结构

		> desc 'm_table'

- 3.查看表行数

		> count 'm_table'

- 4.hdfs查看对应的结构

		hadoop fs -ls /hbase/data/default/m_table/xxxx
	
	xxx代表region，更多信息可以在浏览器上查看

	http://master:60010/table.jsp?name=m_table



# 三、操作表数据：
- 1.插入数据：

		> put 'm_table', '1001', 'meta_data:name', 'zhang3'
		> put 'm_table', '1001', 'meta_data:age', '18'
		> put 'm_table', '1002', 'meta_data:name', 'li4'
		> put 'm_table', '1002', 'meta_data:gender', 'male'

	若想此时在hdfs上进行查看，需

		> flush 'm_table'

- 2.修改
	
		> put 'm_table', '1001', 'meta_data:age', '19'

- 3.分裂region

		> split 'm_table', '49a0707dfd832791eeca0317bb720247'

- 4.合并region

		> merge_region 'd1b66fa0f9a07dc9432a787a41eaf45d', 'd4510bab166ced602b05232a62f4feb2', true

# 四、查询表数据：
- 1.全表扫描(性能差)

		> scan 'm_table'

- 2.根据rowkey查看

		> get 'm_table', '1001'

- 3.根据时间戳查看

		> get 'm_table', '1001', {COLUMN=>'meta_data:age', TIMESTAMP=>1588690735078}
		> get 'm_table', '1001', {COLUMN=>'meta_data:age', TIMESTAMP=>1588693015515}

- 4.获取多个版本数据

		> get 'm_table', '1001', {COLUMN=>'meta_data:age', VERSIONS=>2}

- 5.条件过滤

	- 5.1值过滤——ValueFilter
 
		可以对当前版本、历史版本进行过滤
	
			# 确定值过滤
			> scan 'm_table',  FILTER=>"ValueFilter(=, 'binary:zhang3')"
			# 匹配值过滤
			> scan 'm_table',  FILTER=>"ValueFilter(=, 'substring:ang')"

	- 5.2列名前缀过滤——ColumnPrefixFilter

			> scan 'm_table', FILTER=>"ColumnPrefixFilter('na') AND ValueFilter(=, 'substring:ang')"

	- 5.3rowKey前缀过滤——PrefixFilter

			> scan "m_table", FILTER=>"PrefixFilter('10')"

	- 5.4rowKey区间——STARTROW、ENDROW

			> scan 'm_table', {STARTROW=>'1002'}
			> scan 'm_table', {STARTROW=>'1002', ENDROW=>'4000'}

	- 5.5组合过滤
		
			> scan "m_table", {STARTROW=>'1002', FILTER=>"PrefixFilter('20')"}

	- 5.6正则过滤

		- 1.插数
		
				> put 'm_table', 'user|4001', 'meta_data:name', 'zhengze'
		- 2.导包

				> import org.apache.hadoop.hbase.filter.RegexStringComparator
				> import org.apache.hadoop.hbase.filter.CompareFilter
				> import org.apache.hadoop.hbase.filter.SubstringComparator
				> import org.apache.hadoop.hbase.filter.RowFilter

		- 3.查询—— 'user|'开头，多个数字结尾

				> scan 'm_table', {FILTER=>RowFilter.new(CompareFilter::CompareOp.valueOf('EQUAL'), RegexStringComparator.new('^user\|\d+$'))}

	<font color=red>scan命令时，"=>"前面的都要大写</font>
