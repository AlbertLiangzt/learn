#!/usr/local/bin/python

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

for i in range(0, 5):
	producer.send('topic_test_cluster', value = ('%d' % i))
	producer.flush()
