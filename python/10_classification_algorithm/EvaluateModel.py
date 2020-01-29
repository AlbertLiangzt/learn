#!/usr/bin/python
# --coding:utf-8--

import sys
import os
import math

# TestDataFile = "nb_data.test"
# ModelFile = "model"
# ResultFile = "result"
TestDataFile = sys.argv[1]
ModelFile = sys.argv[2]
ResultFile = sys.argv[3]
WordDic = {}
WordPriorProb = {}
ArticlePriorProb = {}
DefaultPriorProb = {}


# 读出模型中的数据
# 文章类型 文章先验概率 词语默认概率 \n  词语id 最大似然估计(词语的先验概率)
def load_model():
    global ArticlePriorProb
    global DefaultPriorProb
    in_file = file(ModelFile, "r")
    in_file_line = in_file.readline().strip()
    items = in_file_line.split(" ")
    len_items = len(items)

    if len_items < 6:
        print "Model Format Error"
        return

    i = 0
    # 文章类型 文章先验概率 词语默认概率
    while i < len_items:
        class_id = int(items[i])
        WordPriorProb[class_id] = {}

        i += 1
        ArticlePriorProb[class_id] = float(items[i])
        i += 1
        DefaultPriorProb[class_id] = float(items[i])
        i += 1

    # 将词语id，词频
    # 词语id 最大似然估计(词语的先验概率)
    for class_id in ArticlePriorProb.keys():
        in_file_line = in_file.readline().strip()
        items = in_file_line.split(" ")
        len_items = len(items)

        i = 0
        while i < len_items:
            word_id = int(items[i])
            if word_id not in WordDic:
                WordDic[word_id] = 1
            i += 1
            WordPriorProb[class_id][word_id] = float(items[i])
            i += 1
    in_file.close()
    print len(ArticlePriorProb), " classes! ", len(WordDic), "words!"


# 预测
def predict():
    global ArticlePriorProb
    global DefaultPriorProb
    true_label_list = []
    predict_label_list = []

    in_file = file(TestDataFile, "r")
    out_file = file(ResultFile, "w")

    score_dic = {}

    in_file_line = in_file.readline().strip()
    # 读取每一列数据class_id, word_id, word_id, word_id...
    # line_count = 0
    while len(in_file_line) > 0:
        pos = in_file_line.find("#")
        if pos > 0:
            in_file_line = in_file_line[:pos].strip()
        # line_count += 1
        # if line_count %10 ==0:
        #     print line_count, " lines finished!\r"

        # 获取真实文章类型
        words = in_file_line.split(" ")
        if len(words) < 1:
            print "Test Data Error!"
            break
        class_id = int(words[0])
        true_label_list.append(class_id)

        # 获取词频
        words = words[1:]
        for class_id in ArticlePriorProb.keys():
            score_dic[class_id] = math.log(ArticlePriorProb[class_id])

        for word in words:
            if len(word) < 1:
                continue
            word_id = int(word)

            if word_id not in WordDic:
                continue
            for class_id in ArticlePriorProb.keys():
                if word_id not in WordPriorProb[class_id]:
                    score_dic[class_id] += math.log(DefaultPriorProb[class_id])
                else:
                    score_dic[class_id] += math.log(WordPriorProb[class_id][word_id])

        # 选出得分最高的class_id作为预测结果

        max_predict_score = max(score_dic.values())
        for class_id in score_dic.keys():
            if score_dic[class_id] == max_predict_score:
                predict_label_list.append(class_id)
        in_file_line = in_file.readline().strip()

    in_file.close()
    out_file.close()
    print len(predict_label_list), len(true_label_list)
    return true_label_list, predict_label_list


# 输出预测结果
def output_result(origin_list, predict_list):
    i = 0
    outfile = file(ResultFile, 'w')
    while i < len(origin_list):
        outfile.write(str(origin_list[i]))
        outfile.write(' ')
        outfile.write(str(predict_list[i]))
        outfile.write('\n')
        i += 1
    outfile.close()


# 评估模型
def evaluate(origin_list, predict_list):
    accuracy = 0
    i = 0
    while i < len(origin_list):
        if origin_list[i] == predict_list[i]:
            accuracy += 1
        i += 1
    # 准确度
    accuracy = float(accuracy) / float(len(origin_list))
    print "Accuracy:", accuracy


load_model()
origin_list, predict_list = predict()
output_result(origin_list, predict_list)
evaluate(origin_list, predict_list)
