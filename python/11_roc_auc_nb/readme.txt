评估方法：
	混淆矩阵——PR，ROC(Receiver Operating Characteristic curve接收者操作特征曲线)，AUC(Area Under Curve ROC曲线下的面积)

ROC结果
无图形	cat auc.raw | sort -t$'\t' -k2g  | awk -F'\t' '($1==-1){++x;a+=y}($1==1){++y}END{print 1.0 - a/(x*y)}'

	x：表示负样本的个数M=50
	y：表示正样本的个数N=20
	a：错误的累加

	x*y = M*N = 1000  <xi, yj>
	如果xi在yj前面，a不累计
	如果xi在yj后面，a累计
	a/(x*y) : 错误率
	1-a/(x*y)：正确率
	
有图形	python plot_roc.py auc.raw