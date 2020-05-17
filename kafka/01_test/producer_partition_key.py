#!/usr/local/bin/python

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

for i in range(0, 10):
	producer.send('topic_test_cluster', key = ('%d' % i), value = b'keyValue')
	producer.flush()
