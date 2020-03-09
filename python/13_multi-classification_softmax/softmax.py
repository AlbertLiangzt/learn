#!/usr/local/bin/python
# -*- coding: UTF-8 -*

import sys
import math
import pandas as pd
import numpy as np
import random

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class Softmax(object):
    def __init__(self):
        self.learning_step = 0.000001  # 学习速率
        self.max_iteration = 1000  # 最大迭代次数
        self.weight_lambda = 0.01  # 衰退权重

    def train(self, features, labels):
        self.k = len(set(labels))  # 去重，类别的总数
        self.w = np.zeros((self.k, len(features[0]) + 1))

        time = 0
        while time < self.max_iteration:
            print ('loop %d' % time)
            time += 1
            index = random.randint(0, len(labels) - 1)

            x = features[index]
            y = labels[index]

            x = list(x)
            x.append(1.0)
            x = np.array(x)

            # 梯度公式
            # 每一个label对应的梯度
            derivatives = []
            for j in range(self.k):
                derivatives.append(self.cal_partial_derivative(x, y, j))

            for j in range(self.k):
                self.w[j] -= self.learning_step * derivatives[j]

    def predict(self, features):
        labels = []
        for feature in features:
            x = list(feature)
            x.append(1)

            x = np.matrix(x)
            x = np.transpose(x)

            labels.append(self.predict_(x))
        return labels

    def cal_partial_derivative(self, x, y, j):
        first = int(y == j)  # 计算示性函数
        second = self.cal_probability(x, j)  # 计算后面那个概率

        # return -x*(first-second)
        # return -x*(first-second) + self.weight_lambda*abs(self.w[j]) # L1:|w|范数 lasso
        # return -x*(first-second) + self.weight_lambda*self.w[j]*self.w[j] #L2: |w^2|范数 ridge
        return -x * (first - second) + self.weight_lambda * self.w[j] * self.w[j] + self.weight_lambda * abs(self.w[j])

    # x的分类为类别j的概率为
    def cal_probability(self, x, j):
        molecule = self.cal_e(x, j)
        denominator = sum([self.cal_e(x, i) for i in range(self.k)])

        return molecule / denominator

    # 内积
    def cal_e(self, x, l):
        theta_l = self.w[l]
        product = np.dot(theta_l, x)

        return math.exp(product)

    def predict_(self, x):
        result = np.dot(self.w, x)
        row, column = result.shape

        # 找最大值所在的列
        _positon = np.argmax(result)
        m, n = divmod(_positon, column)

        return m


if __name__ == '__main__':
    print ('Start read data')

    raw_data = pd.read_csv('./train.csv', header=0)
    data = raw_data.values

    imgs = data[0::, 1::]
    labels = data[::, 0]

    # 选取2/3数据作为训练集，1/3作为测试集
    # 将矩阵随机划分为训练子集和测试子集，并返回划分好的训练集测试集样本和训练集测试集标签
    train_features, test_features, train_labels, test_labels = train_test_split(imgs, labels, test_size=0.33,
                                                                                random_state=1)

    print train_features.shape
    print test_features.shape

    print ('start training')
    p = Softmax()
    p.train(train_features, train_labels)

    print('Start predicting')
    test_predict = p.predict(test_features)

    print
    p.w.shape
    # print p.w[0]

    score = accuracy_score(test_labels, test_predict)
    print("The accruacy socre is " + str(score))
