#!/usr/local/bin/python
from kafka import KafkaConsumer

def main():
	consumer = KafkaConsumer(b'flume_kafka', group_id=b'my_group_id', bootstrap_servers=['master:9092', 'slave1:9092', 'slave2:9092'], auto_offset_reset='earliest')
	for msg in consumer:
		print(msg)

if __name__ == '__main__':
	main()
