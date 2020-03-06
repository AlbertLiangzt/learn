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

    def train(self, features, labels):
        self.k = len(set(labels))
        self.w = np.zeros(self.k, len(features[0] + 1))

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

            derivatives = [self.cal_partial_derivative(x, y, j) for j in range(self.k)]

            for j in range(self.k):
                self.w[j] -= self.learning_step * derivatives[j]


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


