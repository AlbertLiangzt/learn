echo "--------close firewall--------"
systemctl stop firewalld
ssh slave1 systemctl stop firewalld
ssh slave2 systemctl stop firewalld

echo "--------time synchronization--------"
ntpdate ntp1.aliyun.com
ssh slave1 ntpdate ntp1.aliyun.com
ssh slave2 ntpdate ntp1.aliyun.com

echo "--------hadoop format--------"
rm -rf /usr/local/src/hadoop-2.6.5/dfs
ssh slave1 rm -rf /usr/local/src/hadoop-2.6.5/dfs
ssh slave2 rm -rf /usr/local/src/hadoop-2.6.5/dfs
hadoop namenode -format

echo "--------start yarn hdfs--------"
sh /usr/local/src/hadoop-2.6.5/sbin/start-all.sh

sleep 10
echo "--------start spark--------"
sh /usr/local/src/spark-1.6.0-bin-hadoop2.6/sbin/start-all.sh
sleep 10

echo "--------start zookeeper--------"
sh /usr/local/src/zookeeper-3.4.5/bin/zkServer.sh start
ssh slave1 /usr/local/src/zookeeper-3.4.5/bin/zkServer.sh start
ssh slave2 /usr/local/src/zookeeper-3.4.5/bin/zkServer.sh start
sleep 10

echo "--------start hbase--------"
sh /usr/local/src/hbase-0.98.6-hadoop2/bin/start-hbase.sh

echo "--------start storm--------"
source activate py27
python /usr/local/src/apache-storm-0.9.3/bin/storm nimbus &
python /usr/local/src/apache-storm-0.9.3/bin/storm ui &
python /usr/local/src/apache-storm-0.9.3/bin/storm logviewer &

ssh slave1 python /usr/local/src/apache-storm-0.9.3/bin/storm supervisor &
ssh slave1 python /usr/local/src/apache-storm-0.9.3/bin/storm logviewer &

ssh slave2 python /usr/local/src/apache-storm-0.9.3/bin/storm supervisor &
ssh slave2 python /usr/local/src/apache-storm-0.9.3/bin/storm logviewer &

echo "--------hadoop cluster startup completed--------"
jps

# kafka
# sh /usr/local/src/kafka_2.11-0.10.2.1/bin/kafka-server-start.sh /usr/local/src/kafka_2.11-0.10.2.1/config/server.properties &
# ssh slave1 sh /usr/local/src/kafka_2.11-0.10.2.1/bin/kafka-server-start.sh /usr/local/src/kafka_2.11-0.10.2.1/config/server.properties &
# ssh slave2 sh /usr/local/src/kafka_2.11-0.10.2.1/bin/kafka-server-start.sh /usr/local/src/kafka_2.11-0.10.2.1/config/server.properties &

