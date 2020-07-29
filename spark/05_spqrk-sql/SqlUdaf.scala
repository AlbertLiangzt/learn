package com.albert.sql

import org.apache.spark.sql.Row
import org.apache.spark.sql.expressions.{MutableAggregationBuffer, UserDefinedAggregateFunction}
import org.apache.spark.sql.hive.HiveContext
import org.apache.spark.sql.types.{DataType, IntegerType, StringType, StructField, StructType}
import org.apache.spark.{SparkConf, SparkContext}

object SqlUdaf {

  def main(args: Array[String]): Unit = {
    val sparkConf = new SparkConf().setMaster("local[2]").setAppName("SparkSqlUdaf")
    val sparkCtx = new SparkContext(sparkConf)

    val hiveCtx = new HiveContext(sparkCtx)
    hiveCtx.table("rating_table").registerTempTable("rating_table")

    hiveCtx.udf.register("strlen", (input: String) => input.length)
    hiveCtx.udf.register("wordCount", new WordCountUdaf)

    hiveCtx.sql("SELECT rating, wordCount(rating) AS count, strlen(rating) as length" +
      " FROM rating_table GROUP BY rating").show()

  }

}

class WordCountUdaf extends UserDefinedAggregateFunction {

  /**
   * 指定输入数据类型
   *
   * @return
   */
  override def inputSchema: StructType = StructType(Array(StructField("input", StringType, true)))

  /**
   * 指定merge处理的类型（缓冲区数据类型）
   *
   * @return
   */
  override def bufferSchema: StructType = StructType(Array(StructField("count", IntegerType, true)))

  /**
   * 指定udaf的返回类型
   *
   * @return
   */
  override def dataType: DataType = IntegerType

  /**
   * 确保一致性：输入和输出相同
   * true:密等函数
   *
   * @return
   */
  override def deterministic: Boolean = true

  /**
   * 在Aggregate之前,每组数据进行初始化（初始化缓冲区）
   *
   * @param buffer
   */
  override def initialize(buffer: MutableAggregationBuffer): Unit = {
    buffer(0) = 0
  }

  /**
   * 计算每组的值，类似MR中的combiner
   *
   * @param buffer1 原本缓冲区的数据
   * @param input   新的输入数据
   */
  override def update(buffer1: MutableAggregationBuffer, input: Row): Unit = {
    buffer1(0) = buffer1.getAs[Int](0) + 1
  }

  /**
   * merge各节点的结果（合并缓冲区）
   *
   * @param buffer1 缓冲区1数据
   * @param buffer2 缓冲区2数据
   */
  override def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = {
    buffer1(0) = buffer1.getAs[Int](0) + buffer2.getAs[Int](0)
  }

  /**
   *
   * @param buffer 最终结果
   * @return 返回udaf结果
   */
  override def evaluate(buffer: Row): Any = buffer.getAs[Int](0)
}

