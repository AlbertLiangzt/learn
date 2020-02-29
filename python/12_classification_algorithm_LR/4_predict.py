# -*- coding: utf-8 -*-
import os
import sys
import numpy as np 
import operator
from numpy import *
from common_libs import *

weights = mat([[4.17881308],[0.50489874],[0.61980264]])
#testdata = mat([-0.147324,2.874846])
#testdata = mat([-2.46015, -6.866805])
testdata = mat([0.931635, -1.589505])
# 0.931635  -1.589505   1.0

m,n = shape(testdata)
testmat = zeros((m,n+1))
testmat[:,0] = 1
testmat[:,1:] = testdata
print classifier(testmat,weights)
#print regression_calc(testmat,weights)
