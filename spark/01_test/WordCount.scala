import org.apache.spark.{SparkConf, SparkContext}

object WordCount {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setMaster("local").setAppName("WordCount")
    val sc = new SparkContext(conf)
    val localPath = "D:/scala/bigData/01_test/src/main/resources"

    val rdd = sc.textFile(localPath + "/WordCount_The_Man_of_Property.txt")
    val data = rdd.flatMap(_.split(" ")) // "_"表示输入
      .map((_, 1)) // "()"表示一个tuple--"(word,1)"
      .reduceByKey(_ + _) // 一个value加上另一个value，此时输出--"(word,count)"
      .map {
        x => x._1 + "\t" + x._2 // 输出“word count”
      }

    data.saveAsTextFile(localPath + "/wordCount_out")

  }
}
