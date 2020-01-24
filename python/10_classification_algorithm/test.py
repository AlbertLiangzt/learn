#!/usr/bin/python

import sys

#infile = file("a.txt", "r")
#for line in infile:
#	ss = line.readline().strip()
#	print ss

def fun_1():
	global a
	a = "1"
	print a, "fun_1"

def fun_2():
	global a
	print a,"fun_2"
	a = "2"
	print a,"fun_2_2"

def fun_3():
	a = "3"
	print a,"fun_3"

fun_1()
fun_2()
fun_3()


