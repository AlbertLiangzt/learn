# -*- coding: utf-8 -*
import sys

cur_word = None
sum_count = 0

for line in sys.stdin:
	ss = line.strip().split('\t')
	if len(ss) != 2:
		continue
	word, cnt = ss

	# 第一次进入时，cur_word为none，赋值
	if cur_word == None:
		cur_word = word

	# map的输出是排好序的，直接比较当前k是否与上一个k相同，相同则加1
	if cur_word != word:
		print '\t'.join([cur_word, str(sum_count)])
		cur_word = word
		sum_count = 0
	sum_count += int(cnt)

# 当倒数第二个k输出完成时，已经跳出循环
# 输出最后一个k
print '\t'.join([cur_word, str(sum_count)])
