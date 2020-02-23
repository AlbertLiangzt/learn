#!/usr/bin/python
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
Input = file2matrix("testSet.txt","\t")
target = Input[:,-1] #获取分类标签列表
[m,n] = shape(Input)

# 按分类绘制散点图
drawScatterbyLabel(plt,Input)

# 构建x+b 系数矩阵：b这里默认为1
dataMat = buildMat(Input)
alpha = 0.001 # 步长
steps = 500  # 迭代次数