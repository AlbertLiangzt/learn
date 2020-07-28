package com.albert.sql

import org.apache.spark.sql.SQLContext
import org.apache.spark.{SparkConf, SparkContext}

object SqlUdf {
  def main(array: Array[String]) {
    val sparkConf = new SparkConf().setMaster("local[2]").setAppName("SparkSqlUdf")
    val sparkCtx = new SparkContext(sparkConf)

    val sqlCtx = new SQLContext(sparkCtx)
    val perInfo = sqlCtx.read.json("hdfs://master:9000/data/person_info.json")

    perInfo.registerTempTable("person_info")

    sqlCtx.udf.register("strlen", (input: String) => input.length)
    sqlCtx.sql("SELECT id, name, strlen(name), age FROM person_info").show()

    //    println(perInfo.schema)

  }

}
