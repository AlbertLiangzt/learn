echo "--------stop storm-------"
kill -9  `ps aux | fgrep storm | fgrep -v 'fgrep' | awk '{print $2}'`
ssh slave1 kill -9 `ps aux | fgrep storm | fgrep -v 'fgrep' | awk '{print $2}'` 
ssh slave2 kill -9 `ps aux | fgrep storm | fgrep -v 'fgrep' | awk '{print $2}'` 

echo "--------stop hbase-------"
sh /usr/local/src/hbase-0.98.6-hadoop2/bin/stop-hbase.sh
sleep 5

echo "--------stop zookeeper-------"
sh /usr/local/src/zookeeper-3.4.5/bin/zkServer.sh stop
ssh slave1 /usr/local/src/zookeeper-3.4.5/bin/zkServer.sh stop
ssh slave2 /usr/local/src/zookeeper-3.4.5/bin/zkServer.sh stop
sleep 10

echo "--------stop spark-------"
sh /usr/local/src/spark-1.6.0-bin-hadoop2.6/sbin/stop-all.sh

echo "--------stop yarn hdfs-------"
sh /usr/local/src/hadoop-2.6.5/sbin/stop-all.sh

echo "--------hadoop cluster startup completed-------"
jps
