#!/usr/local/bin/python
# -*- coding:utf-8 -*

import sys

sys.path.append('../../')

import jieba

aa = jieba.cut('只是随便耍耍这个python的jieba', cut_all=False)
print (' '.join(aa))
