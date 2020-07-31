## 文件说明

- SqlTest.scala 从hdfs的原始text中读数据
- SqlJson.scala 从hdfs中的json文件读数据
- SqlHive.scala 从hive中读数据
- SqlUdf.scala 从json中读数据，并进行udf操作
- SqlUdaf.scala 从hive中读数据，并进行udaf操作

- sql-1.0.SNAPSHOT.jar 以上的scala编译成的jar包

- sql_**.sh 对应的sparksql在linux下的执行命令
- sparksql_terminal.sh 进入spark_sql的终端

- pom.xml pom文件

## 注意
1、运行sql_hive的时候需要添加mysql的connector

2、需要把Hive/conf的hive-site.xml文件，复制到spark/conf目录下(为了运行hiveContext.sql)

不然会报错
<font color=red>
Exception in thread "main" org.apache.spark.sql.AnalysisException: Table not found：TABLE_NAME; line 1 pos 27
</font>
