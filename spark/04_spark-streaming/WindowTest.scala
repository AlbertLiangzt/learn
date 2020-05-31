package com.albert.streaming.test

import org.apache.spark.SparkConf
import org.apache.spark.storage.StorageLevel
import org.apache.spark.streaming.{Seconds, StreamingContext}

object WindowTest {
  def main(args: Array[String]): Unit = {
    val sparkConf = new SparkConf().setAppName("StreamingWindowTest")
    val streamCtx = new StreamingContext(sparkConf, Seconds(10))
    streamCtx.checkpoint("hdfs://master:9000/hdfs_checkpoint")

    val lines = streamCtx.socketTextStream(args(0), args(1).toInt, StorageLevel.MEMORY_AND_DISK_SER)
    val words = lines.flatMap(_.split(" "))
    val wordCounts = words.map(x => (x, 1)).reduceByKeyAndWindow((v1: Int, v2: Int) => v1 + v2, Seconds(30), Seconds(10))

    wordCounts.print()
    streamCtx.start()
    streamCtx.awaitTermination()

  }

}
