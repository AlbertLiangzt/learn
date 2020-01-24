#!/usr/local/bin/python
# -*- coding: UTF-8 -*

import sys, os

file_path_dir = sys.argv[1]

# 执行打开读取文件的命令
def read_file_handler(f):
	fd = open(f, 'r')
	return fd

file_name = 0

for fd in os.listdir(file_path_dir):
	# 获取到所有的 文件路径/文件名
	file_path_name = file_path_dir + '/' + fd
	content_list = []

	file_fd = read_file_handler(file_path_name)
	# 把每一篇文章拼接成一行
	for line in file_fd:
		content_list.append(line.strip())

	# 给定每一篇文章一个序号
	print '\t'.join([str(file_name), ' '.join(content_list)])

	file_name += 1

