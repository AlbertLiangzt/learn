#!/usr/bin/python
# --coding:utf-8--

import sys
import os
import random

WordList = []
WordIdDic = {}
TrainingPercent = 0.8

# in_path = ("./data/")
# OutFileName = ("nb_data")
in_path = sys.argv[1]
OutFileName = sys.argv[2]
trainOutFile = file(OutFileName + ".train", "w")
testOutFile = file(OutFileName + ".test", "w")


def convertData():
    i = 0
    tag = 0
    for file_name in os.listdir(in_path):

        # 将所有的文件按名字打标签，business-1，auto-2，sport-3
        if file_name.find("business") != -1:
            tag = 1
        elif file_name.find("auto") != -1:
            tag = 2
        elif file_name.find("sport") != -1:
            tag = 3

        # 将80%的文件作为训练集，将20%的文件作为测试集
        i += 1
        rand = random.random()
        out_file = testOutFile
        if rand < TrainingPercent:
            out_file = trainOutFile

        # 每输出100个文件，打印一下进度
        # if i % 100 == 0:
        #     print i, "files processed!\r"

        in_file = file(in_path + "/" + file_name, "r")
        content = in_file.read().strip()
        content = content.decode("utf-8", "ignore")
        words = content.replace("\n", " ").split(" ")
        out_file.write(str(tag) + " ")

        # 读取文章，将不重复的词放入词典，生成id
        # 将文章的词语变成id输出
        for word in words:
            if len(word.strip()) < 1:
                continue
            if word not in WordIdDic:
                WordList.append(word)
                WordIdDic[word] = len(WordList)
            out_file.write(str(WordIdDic[word]) + " ")
        out_file.write("#" + file_name + "\n")
        in_file.close()
    print i, "files loaded!"
    print len(WordList), "unique words found!"


convertData()
trainOutFile.close()
testOutFile.close()
