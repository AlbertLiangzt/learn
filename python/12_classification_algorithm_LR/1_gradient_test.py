# -*- coding: utf-8 -*-
import os
import sys
import math
import numpy as np
import operator
from numpy import *
from common_libs import *
import matplotlib.pyplot as plt

# 输入数据
Input = file2matrix("testSet1.txt", "\t")
target = Input[:, -1]  # 获取分类标签列表
[m, n] = shape(Input)  # m-行数 n-列数


# 按分类绘制散点图
drawScatterbyLabel(plt, Input)

# 构建x+b 系数矩阵：b这里默认为1
dataMat = buildMat(Input)  # 矩阵的第一列都为1
alpha = 0.001  # 步长
steps = 500  # 迭代次数

weights = ones((n, 1))  # 初始化权重向量

# 主程序
for k in xrange(steps):
    # wx
    gradient = dataMat * mat(weights)
    # sigmoid(wx)
    output = logistic(gradient)  # logistic function
    errors = target - output  # 计算误差
    weights = weights + alpha * dataMat.T * errors

print weights  # 输出权重

X = np.linspace(-5, 5, 100)
Y = -(double(weights[0]) + X * (double(weights[1]))) / double(weights[2])
plt.plot(X, Y)
plt.show()
