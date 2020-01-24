#!/usr/local/bin/python

import sys

def getMax(first_str, second_str):
	len_vv = [[0]*50] * 50

	first_str = unicode(first_str, "utf-8", errors='ignore')
	second_str = unicode(second_str, "utf-8", errors='ignore')

	len_first = len(first_str.strip())
	len_second = len(second_str.strip())

	for i in range(1, len_first+1):
		for j in range(1, len_second+1):
			if first_str[i-1] == second_str[j-1]:
				len_vv[i][j] = 1 + len_vv[i-1][j-1]
			else:
				len_vv[i][j] = max(len_vv[i-1][j], len_vv[i][j-1])
	return float(float(len_vv[len_first][len_second]) * 2/ float(len_first + len_second))


for line in sys.stdin:
    ss = line.strip().split('\t')
    if len(ss) != 2:
        continue
    first_str = ss[0].strip()
    second_str = ss[1].strip()

    sim_score = getMax(first_str, second_str)
    print '\t'.join([first_str, second_str, str(sim_score)])

