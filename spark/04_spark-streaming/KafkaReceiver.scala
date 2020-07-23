package com.albert.streaming.kafka

import org.apache.spark.SparkConf
import org.apache.spark.storage.StorageLevel
import org.apache.spark.streaming.dstream.{DStream, ReceiverInputDStream}
import org.apache.spark.streaming.kafka.KafkaUtils
import org.apache.spark.streaming.{Seconds, StreamingContext}

object KafkaReceiver {
  def updateFunction(currentValues: Seq[Int], preValues: Option[Int]): Option[Int] = {
    val current = currentValues.sum
    val pre = preValues.getOrElse(0)
    Some(current + pre)
  }

  def main(args: Array[String]): Unit = {
    val sparkConf = new SparkConf().setAppName("StreamingWordCountKafkaReceiver")
    val streamCtx = new StreamingContext(sparkConf, Seconds(5))
    streamCtx.checkpoint("hdfs://master:9000/hdfs_checkpoint")

    val zk = "master:2181,slave1:2181,slave2:2181"
    val groupId = "group_1"

    val topicAndLine: ReceiverInputDStream[(String, String)] =
      KafkaUtils.createStream(streamCtx, zk, groupId, Map("topic_kafka" -> 1), StorageLevel.MEMORY_AND_DISK_SER)

    val lines: DStream[String] = topicAndLine.map { x => x._2 }
    val words = lines.flatMap(_.split(" "))
    val wordCounts = words.map(x => (x, 1)).updateStateByKey(updateFunction _)
    wordCounts.print()
    streamCtx.start()
    streamCtx.awaitTermination()

  }

}
