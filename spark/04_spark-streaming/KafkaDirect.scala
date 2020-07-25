package com.albert.streaming

//import kafka.serializer.StringDecoder
import _root_.kafka.serializer.StringDecoder
import org.apache.spark.SparkConf
import org.apache.spark.streaming.kafka.KafkaUtils
import org.apache.spark.streaming.{Seconds, StreamingContext}

object KafkaDirect {
  def main(args: Array[String]) {
    val sparkConf = new SparkConf().setAppName("StreamingWordCountKafkaDirect")
    val streamCtx = new StreamingContext(sparkConf, Seconds(5))

    val brokers = "master:9092"
    val topic = "topic_kafka"
    val topicSet = topic.split(",").toSet
    val kafkaParam = Map[String, String]("metadata.broker.list" -> brokers)
    val msg = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](streamCtx, kafkaParam, topicSet)

    val lines = msg.map(_._2)
    val words = lines.flatMap(_.split(" "))
    val wordCounts = words.map(x => (x, 1)).reduceByKey(_ + _)
    wordCounts.print()
    streamCtx.start()
    streamCtx.awaitTermination()

  }

}

