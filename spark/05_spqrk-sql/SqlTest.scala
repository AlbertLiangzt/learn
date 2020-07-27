package com.albert.sql

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.{Row, SQLContext}
import org.apache.spark.sql.types.{StringType, StructField, StructType}

import scala.collection.mutable

object SqlTest {
  def main(args: Array[String]) {

    val studentSchema: StructType = StructType(mutable.ArraySeq(
      StructField("Sno", StringType, nullable = false),
      StructField("Sname", StringType, nullable = false),
      StructField("Sgender", StringType, nullable = false),
      StructField("Sbirth", StringType, nullable = true),
      StructField("Sclass", StringType, nullable = true)
    ))

    val sparkConf = new SparkConf().setMaster("local[2]").setAppName("SparkSqlTest")
    val sparkCtx = new SparkContext(sparkConf)
    val sqlCtx = new SQLContext(sparkCtx)

    val studendData = sparkCtx.textFile("hdfs://master:9000/sql/sql_stu.data").map{
      lines =>
        val line = lines.split(",")
        Row(line(0),line(1),line(2),line(3),line(4),line(5))
    }

    val studentTable = sqlCtx.createDataFrame(studendData, studentSchema)
    studentTable.registerTempTable("student")

    sqlCtx.sql("SELECT Sname, Sgender, Sclass FROM student").show()

  }

}
