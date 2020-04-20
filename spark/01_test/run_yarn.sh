
/usr/local/src/hadoop-2.6.5/bin/hadoop fs -rmr /userWatchList_out

/usr/local/src/spark-1.6.0-bin-hadoop2.6/bin/spark-submit \
	--master yarn-cluster \
	--num-executors 2 \
	--executor-memory 1g \
	--executor-cores 1 \
	--driver-memory 1g \
	--class UserWatchList /usr/local/src/learn/albert/15_scala_test/com.albert.scala.test-1.0-SNAPSHOT.jar




