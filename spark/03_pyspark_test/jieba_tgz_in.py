#!/usr/local/bin/python
# --coding:utf-8--

import sys

from pyspark import SparkContext, SparkConf

reload(sys)
sys.path.append('../../')
sys.setdefaultencoding('utf-8')

import jieba

# 本地测试
# input_path = "./"
# output_path = "./"


# 集群测试
input_path = ""
output_path = ""


def split(x):
    return x.strip().split("    ")


def fenci(x):
    word_list = jieba.cut(x.strip())
    ls = []
    ls.append(x.strip())
    for word in word_list:
        ls.append(word)
    return ls


if __name__ == "__main__":
    conf = SparkConf().setMaster("spark://master:7077").setAppName("jieba_tgz_in")
    sc = SparkContext(conf=conf)
    sc.addFile("jieba.tgz")

    in_file = (input_path + "/music_meta.txt.small")
    rdd = in_file \
        .map(lambda x: x.strip().split(" ")) \
        .map(lambda x: x[1].strip()) \
        .map(fenci) \
        .map(lambda x: " ".join(x)) \
        .saveAsTextFile(output_path + "/jieba_tgz_in")
    sc.stop()
