package com.albert.sql

import org.apache.spark.sql.hive.HiveContext
import org.apache.spark.{SparkConf, SparkContext}

object SqlHive {
  def main(args:Array[String]) {
    val sparkConf = new SparkConf().setMaster("local[2]").setAppName("SparkSqlHive")
    val sparkCtx = new SparkContext(sparkConf)

    val hiveCtx = new HiveContext(sparkCtx)
    hiveCtx.sql("SELECT movieid, title FROM movie_table").show()
  }

}
