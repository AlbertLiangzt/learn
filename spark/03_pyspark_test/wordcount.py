#!/usr/local/bin/python
# --coding:utf-8--

from pyspark import SparkContext, SparkConf

# 本地测试
input_path = "./"
output_path = "./"
# 集群测试
# input_path = ""
# output_path = ""


def sp(x):
    return x.strip().split(" ")


if __name__ == "__main__":
    conf = SparkConf().setMaster("local").setAppName("word_count")
    sc = SparkContext(conf=conf)

    in_file = sc.textFile(input_path + "/The_Man_of_Property.txt")
    rdd = in_file \
        .flatMap(sp) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a + b) \
        .map(lambda x: " ".join([x[0], str(x[1])])) \
        .saveAsTextFile(output_path + "/wordCount_out")

    # result = rdd.collect()
    #
    # for line in result:
    #     print(line)
    sc.stop()
