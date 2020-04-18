import org.apache.spark.{SparkConf, SparkContext}

object UserWatchList {
  def main(args: Array[String]): Unit = {
    //    val localPath = "D:/scala/bigData/01_test/src/main/resources" // 本地测试地址
    val localPath = "" // 集群测试地址
    val conf = new SparkConf()
    //    conf.setMaster("local")
    conf.setAppName("UserWatchList")
    val sc = new SparkContext(conf)

    val rdd = sc.textFile(localPath + "/user_item_score.data")
    val data = rdd.filter { x =>
      val fileds = x.split("\t") // userid, itemid, score
      fileds(2).toDouble > 2 // 过滤低于2分的
    }.map { x =>
      val fileds = x.split("\t")
      (fileds(0), (fileds(1), fileds(2))) // (userId, (itemId, score))
    }.groupByKey(10) // (userId, CompactBuffer((itemId, score), (itemId, score)))
      .map { x =>
        val userId = x._1
        val itemId_score_tuple_list = x._2
        val tem_arr = itemId_score_tuple_list.toArray.sortWith(_._2 > _._2) // 根据score排序

        // 取前五个数据
        var watchLen = tem_arr.length
        if (watchLen > 5) {
          watchLen = 5
        }

        // 输出itemId:score
        val strBuf = new StringBuilder
        // for (i <- 1 to watchLen) { // 最多[1,2,3,4,5]
        for (i <- 0 until watchLen) { // 最多[0,1,2,3,4,5)
          strBuf ++= tem_arr(i)._1 // 取数组下标为i的 第一个数itemId
          strBuf.append(":")
          strBuf ++= tem_arr(i)._2 // 取数组下标为i的 第一个数score
          strBuf.append(" ")
        }
        userId + "\t" + strBuf
      }

    // 分区，会有三个输出part-00000 part-00001 part-00002
    //data.repartition(3).saveAsTextFile("D:/scala/bigData/01_test/src/main/resources/userWatchList_out")
    data.saveAsTextFile(localPath + "/userWatchList_out")

  }
}
