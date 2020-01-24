lcs Longest Common Subsequence最长公共子序列

两个序列的公共子序列中，长度最长的那个，为最长公共子序列
最长公共子串要求连接
X：acdfg
Y：adfc
lcs：adf

算法：
求最长公共子序列，二维数组,
xi，yi不相等时，取xi，yi左侧或者上侧最大的数，
xi，yi相等时，取xi，yi左上方的值，并加1
c(i,j)
max{ c(i-1,j), c(i, j-1) }	xi != yi
c(i-1, j-1) +1			xi == yi


脚本：
不需要reduce处理，只需要遍历对比数组中的每个值，就能确定
