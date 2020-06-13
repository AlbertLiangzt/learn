/usr/local/src/spark-1.6.0-bin-hadoop2.6/bin/spark-submit \
	--master local[2] \
	--class com.albert.streaming.kafka.KafkaTest /usr/local/src/learn/albert/25_spark_streaming/streaming-1.0-SNAPSHOT.jar \
	--jars /usr/local/src/spark-1.6.0-bin-hadoop2.6/lib/spark-streaming-kafka_2.10-1.6.0.jar \
	master \
	9999
