#!/usr/local/bin/python
# --coding:utf-8--

from kafka import KafkaConsumer
from kafka import TopicPartition
from kafka.structs import OffsetAndMetadata
from kafka.structs import TopicPartition

def main():
    consumer = KafkaConsumer('topic_test_cluster', bootstrap_servers=['master:9092'])

    print consumer.partitions_for_topic('topic_test_cluster')
    print consumer.topics()
    print consumer.subscription()
    print consumer.assignment()
    print consumer.beginning_offsets(consumer.assignment())

    # 读取partition为2、偏移量从5开始的数据
    consumer.seek(TopicPartition(topic = u'topic_test_cluster', partition = 2), 5)

    for msg in consumer:
        print ('%s:%d:%d: key=%s value=%s' % (msg.topic, msg.partition, msg.offset, msg.key, msg.value))

if __name__ == '__main__':
    main()