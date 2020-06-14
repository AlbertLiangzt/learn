package com.albert.sql

import org.apache.spark.sql.Row
import org.apache.spark.sql.types._
import scala.collection.mutable
import org.apache.spark.{SparkConf, SparkContext}

object sqlTest {
  def main(args: Array[String]) {

    val StudentSchema: StructType = StructType(mutable.ArraySeq(
      StructField("Sno", StringType, nullable = false),
      StructField("Sname", StringType, nullable = false),
      StructField("Ssex", StringType, nullable = false),
      StructField("Sbirthday", StringType, nullable = true),
      StructField("SClass", StringType, nullable = true)
    ))

    val sparkConf = new SparkConf().setMaster("local[2]").setAppName("sqltest")
    val sc = new SparkContext(sparkConf)

    val sqlContext = new org.apache.spark.sql.SQLContext(sc)

    val StudentData = sc.textFile("hdfs://master:9000/sql_stu.data").map{
      lines =>
        val line = lines.split(",")
        Row(line(0),line(1),line(2),line(3),line(4))
    }

    val StudentTable = sqlContext.createDataFrame(StudentData, StudentSchema)
    StudentTable.registerTempTable("Student")

    sqlContext.sql("SELECT Sname, Ssex, SClass FROM Student").show()
  }
}
