package com.albert.streaming.test

import org.apache.spark.SparkConf
import org.apache.spark.storage.StorageLevel
import org.apache.spark.streaming.{Seconds, StreamingContext}

object WordCount {
  def main(args: Array[String]): Unit = {
    if (args.length<2) {
      System.err.println("Usage: wordCount <hostname> <port>")
      System.exit(1)
    }

    val sparkConf = new SparkConf().setAppName("wordCount")
    val streamCtx = new StreamingContext(sparkConf, Seconds(5));

    val lines = streamCtx.socketTextStream(args(0), args(1).toInt, StorageLevel.MEMORY_AND_DISK_SER)
    val words = lines.flatMap(_.split(" "))
    val wordCounts = words.map(x => (x,1)).reduceByKey(_+_)
    wordCounts.print()
    wordCounts.saveAsTextFiles("hdfs://master:9000/stream_out", "doc")
    streamCtx.start()
    streamCtx.awaitTermination()

  }

}
