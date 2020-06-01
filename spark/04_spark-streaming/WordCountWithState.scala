package com.albert.streaming.test

import org.apache.spark.SparkConf
import org.apache.spark.storage.StorageLevel
import org.apache.spark.streaming.{Seconds, StreamingContext}

object WordCountWithState {
  def updateFunction(currentValues: Seq[Int], preValues: Option[Int]): Option[Int] = {
    val current = currentValues.sum
    val pre = preValues.getOrElse(0)
    Some(current + pre)
  }

  def main(args: Array[String]) {
    if (args.length < 2) {
      System.err.println("Usage:WordCountWithState<hostname> <port>")
      System.exit(1)
    }

    val sparkConf = new SparkConf().setAppName("StreamingWordCountWithState")
    val streamCtx = new StreamingContext(sparkConf, Seconds(5))
    streamCtx.checkpoint("hdfs://master:9000/hdfs_checkpoint")

    val lines = streamCtx.socketTextStream(args(0), args(1).toInt, StorageLevel.MEMORY_AND_DISK_SER)
    val words = lines.flatMap(_.split(" "))
    val wordCounts = words.map(x => (x, 1)).updateStateByKey(updateFunction _)

    wordCounts.print()
    wordCounts.saveAsTextFiles("hdfs://master:9000/stream_state_out", "doc")
    streamCtx.start()
    streamCtx.awaitTermination()
  }

}
