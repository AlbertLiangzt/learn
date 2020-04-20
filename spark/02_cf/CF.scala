import org.apache.spark.{SparkConf, SparkContext}

import scala.collection.JavaConverters._
import scala.collection.mutable.ArrayBuffer
import scala.math.pow
import scala.math.sqrt

/**
 * 此系统优化点
 *
 * 1.用户打分的物品过多，做了截断；相应的，物品被太多用户打分，也要做截断
 *
 * 2.生成pair对时，如果物品过多，for循环会很耗时
 */
object CF {
  def main(args: Array[String]): Unit = {
    val USER_MAX_LEN = 20 // 用户最大打分个数——用户对多个物品有打分，只取这么多条
    val USER_TOP_LEN = 5 // 只取得分最高的
    val localPath = "D:/scala/bigData/01_test/src/main/resources" // 本地测试地址

    val conf = new SparkConf()
    conf.setMaster("local")
    conf.setAppName("CF")

    val sc = new SparkContext(conf)
    val line = sc.textFile(localPath + "/user_item_score.data") // userId, itemId, score

    // step1 normalization
    val uiRdd = line.map { x =>
      val fileds = x.split("\t")
      (fileds(0).toString, (fileds(1).toString, fileds(2).toDouble))
    }.groupByKey().flatMap { x => // 1.1将输入数据进行转置，输出item list(user, score)
      val userId = x._1
      val itemScoreList = x._2
      val itemScoreArr = itemScoreList.toArray

      var itemScoreArrLen = itemScoreArr.length
      if (itemScoreArrLen > USER_MAX_LEN) {
        itemScoreArrLen = USER_MAX_LEN
      }

      // 转置，输出(item, (user, score))
      var itemUserScoreArr = new ArrayBuffer[(String, (String, Double))]
      for (i <- 0 until itemScoreArrLen) {
        itemUserScoreArr += ((itemScoreArr(i) _1, (userId, itemScoreArr(i) _2)))
      }
      itemUserScoreArr // 作为下行groupByKey的输入
    }.groupByKey().flatMap { x => // 1.2将score进行归一化操作，并重新输出user item score_new
      val itemId = x._1
      val userScoreList = x._2
      val userScoreArr = userScoreList.toArray
      val userScoreArrLen = userScoreArr.length

      var scoreSum: Double = 0.0
      for (i <- 0 until userScoreArrLen) {
        scoreSum += pow(userScoreArr(i)._2, 2)
      }
      scoreSum = sqrt(scoreSum)

      // 输出新的(user (item, score_new))
      var userItemScoreArr = new ArrayBuffer[(String, (String, Double))]
      for (i <- 0 until userScoreArrLen) {
        userItemScoreArr += ((userScoreArr(i)._1, (itemId, userScoreArr(i)._2 / scoreSum)))
      }.asJava
      userItemScoreArr
    }.groupByKey()

    // step2 generate pairs
    val iiPairRdd = uiRdd.flatMap { x =>
      val itemScoreArr = x._2.toArray

      var itemItemScorePair = new ArrayBuffer[((String, String), Double)]
      for (i <- 0 until itemScoreArr.length - 1) {
        for (j <- i + 1 until itemScoreArr.length) {
          itemItemScorePair += (((itemScoreArr(i)._1, itemScoreArr(j)._1), itemScoreArr(i)._2 * itemScoreArr(j)._2))
          itemItemScorePair += (((itemScoreArr(j)._1, itemScoreArr(i)._1), itemScoreArr(i)._2 * itemScoreArr(j)._2))
        }
      }

      itemItemScorePair
    }.groupByKey() // ((item1, item2), list(score1, score2, score3...))

    // step3 generate result
    iiPairRdd.map { x =>
      val iiPair = x._1
      val scoreList = x._2

      val scoreArray = scoreList.toArray

      var score: Double = 0.0
      for (i <- 0 until scoreArray.length) {
        score += scoreArray(i)
      }

      (iiPair._1, (iiPair._2, score))
    }.groupByKey() // (item1, list(item2, score2)(item3,score3)
      .map { x =>
        val itemId = x._1
        val itemScoreList = x._2
        val scoreArrWithSort = itemScoreList.toArray.sortWith(_._2 > _._2)

        var scoreArrLen = scoreArrWithSort.length
        if (scoreArrLen > USER_TOP_LEN) {
          scoreArrLen = USER_TOP_LEN
        }
        val sb = new StringBuilder
        for (i <- 0 until scoreArrLen) {
          val item = scoreArrWithSort(i)._1
          val score = "%1.4f" format scoreArrWithSort(i)._2
          sb.append(item + ":" + score)
          sb.append(",")
        }
        itemId + "\t" + sb
      }.saveAsTextFile(localPath + "/cf_out")

  }

}
