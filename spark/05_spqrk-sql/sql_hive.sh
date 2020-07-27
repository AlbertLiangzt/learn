/usr/local/src/spark-1.6.0-bin-hadoop2.6/bin/spark-submit \
	--master local[1] \
	--jars /usr/local/src/spark-1.6.0-bin-hadoop2.6/lib/mysql-connector-java-5.1.41-bin.jar \
	--class com.albert.sql.SqlHive /usr/local/src/learn/albert/26_spark_sql/sql-1.0-SNAPSHOT.jar

