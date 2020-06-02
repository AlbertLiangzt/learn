/usr/local/src/spark-1.6.0-bin-hadoop2.6/bin/spark-submit \
	--master local[2] \
	--class com.albert.streaming.test.WordCount /usr/local/src/learn/albert/25_spark_streaming/streaming-1.0-SNAPSHOT.jar \
	master \
	9999

