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