#!/usr/bin/python
# --coding:utf-8--

import sys

# TrainingDataFile = "nb_data.train"
# ModelFile = "nb_data.model"
TrainingDataFile = sys.argv[1]
ModelFile = sys.argv[2]
# 文章类型字典
ClassDic = {}
# 文章先验概率
ArticlePriorProb = {}
# 最大似然估计maximum likehood estimation MLE——每个词的先验概率
WordPriorProb = {}
# 文章每类个数
ClassFreq = {}
# 文本特征字典
WordDic = {}
# 初始频率，未出现过的词的词频
DefaultFreq = 0.1
# 初始概率，未出现过的词的概率
DefaultPriorProb = {}


# 读取训练数据
def loadData():
    i = 0
    in_file = file(TrainingDataFile, "r")
    in_file_ine = in_file.readline().strip()
    while len(in_file_ine) > 0:
        # 过滤无效格式的训练数据，将训练数据按空格切割
        pos = in_file_ine.find("#")
        if pos > 0:
            in_file_ine = in_file_ine[:pos].strip()
        words = in_file_ine.split(" ")
        if len(words) < 1:
            print "Data Format Error!"
            break

        # 获取文章类型
        class_id = int(words[0])
        if class_id not in ClassDic:
            ClassDic[class_id] = {}
            WordPriorProb[class_id] = {}
            ClassFreq[class_id] = 0
        ClassFreq[class_id] += 1
        words = words[1:]

        # 获取文章文本特征
        # 将未出现的词语存在WordDic中word_id:
        # 统计词语出现的次数，存在ClassDic中class_id:(word_id:count)
        # 最大似然——特征x和类别y，在训练数据中同时出现的次数
        for word in words:
            if len(word) < 1:
                continue
            word_id = int(word)
            if word_id not in WordDic:
                WordDic[word_id] = 1
            if word_id not in ClassDic[class_id]:
                ClassDic[class_id][word_id] = 1
            else:
                ClassDic[class_id][word_id] += 1
        i += 1
        in_file_ine = in_file.readline().strip()
    in_file.close()
    print i, "instances loaded!"
    print len(ClassFreq), " classes!", len(WordDic), " words!"


# 求先验概率
def computeModel():
    article_sum = 0.0
    for freq in ClassFreq.values():
        article_sum += freq
    for class_id in ClassFreq.keys():
        # p(yi) = 每类文章个数 / 文章总数
        ArticlePriorProb[class_id] = float(ClassFreq[class_id]) / float(article_sum)

    # p(xj|yi)
    # 遍历每类文章，重构
    for class_id in ClassDic.keys():
        word_sum = 0.0
        # 求出该类文章中，所有词语出现的次数
        for word_id in ClassDic[class_id].keys():
            word_sum += ClassDic[class_id][word_id]
        word_sum += DefaultFreq

        # 求出该类文章中每个词的先验概率
        for word_id in ClassDic[class_id].keys():
            WordPriorProb[class_id][word_id] = float(ClassDic[class_id][word_id] + DefaultFreq) / float(word_sum)
            DefaultPriorProb[class_id] = float(DefaultFreq) / float(word_sum)
    return


# 保存模型
# 文章类型 文章先验概率 词语默认概率 \n  词语id 最大似然估计(词语的先验概率)
def saveModel():
    out_file = file(ModelFile, "w")
    for class_id in ClassFreq.keys():
        out_file.write(str(class_id))
        out_file.write(" ")
        out_file.write(str(ArticlePriorProb[class_id]))
        out_file.write(" ")
        out_file.write(str(DefaultPriorProb[class_id]))
        out_file.write(" ")
    out_file.write("\n")

    for class_id in ClassDic.keys():
        for word_id in ClassDic[class_id].keys():
            out_file.write(str(word_id) + " " + str(WordPriorProb[class_id][word_id]))
            out_file.write(" ")
        out_file.write("\n")
    out_file.close()


loadData()
computeModel()
saveModel()
