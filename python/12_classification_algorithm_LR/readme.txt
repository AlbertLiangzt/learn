二分类(Logistic Regression 逻辑斯谛回归 简称LR)：model -> 0/1
多分类(Softmax)：model -> 0/1/2...

评估方式：PR曲线——确定阈值（人工设定）

sigmoid函数——逻辑回归的实现——推导出来的函数与SIGMOD函数相同
	                1
	𝜂(𝑡)=-------------
	          1+exp(-t)

负对数似然(formula.png)：
	L(w) = - Σ(I(yi=1)log(p(yi=1|xi,w))+ I(yi=0) log(p(yi=0|xi,w)))
	        =- Σ(I(yi=1)log(𝜂(wxi)) +I(yi=0)log(1-𝜂(wxi)))

	I(x):符号函数
	    x条件成立=1
	    x条件不成立 != 1

梯度(formula.png)：
	𝛻L(w)=-Σ(yi-𝜂(wxi))xi
	梯度方向-让f(x,y)函数快速变大的方向
	反梯度方向-让f(x,y)函数快速变小的方向

场景：一个人出现在山谷的任意位置，求走到谷底的最佳路线
方法：梯度下降法—最小化F(w)
	1.设置初始w，计算出F(w)
	2.计算梯度𝛻F(w)
		下降方向：dir=(-𝛻F(w))
	3.尝试梯度更新
		w(new)=w+步长*dir 得到下降后的w(new)和F(w(new))
	4.如果F(w(new))-F(w)较小（基本处于底部，模型稳定 ），停止
		否则w=w(new),F(w)=F(w(new))，继续第二步

目标：
误差=真实值-预测值=(yi-𝜂(wxi))
errors = target - prediction
prediction=sigmoid(wx)=𝜂(wx)
wx=weight * x + b
w1：随机初始化——>f(x) ：预测值
(详细公式见formula.png)


python 1_gradient_calculate.py
	计算模型
python 2_weight_list.py
	将每步的权重记录下来，并在散点图上展示
python 3_weight_change.py
	画出权重变化曲线
python 4_predict.py
	给定数据，预测结果
python 5_SGD.py
	SGD计算

-------------------------
BGD (Batch Gradient Descent批量梯度下降)	
优点：每次迭代遍历所有样本，共同决定最优方向
缺点：样本数量大时，耗时大、占用内存大

SGD (Stochastic Gradient Descent随机梯度下降)
  每次从训练样本中抽取一个样本进行更新，每次都不用遍历所有数据
优点：迭代速度快
缺点：需要迭代更多次数、每次选取方向不一定是最优

MBGD(Mini-batch Gradient Descent小批量梯度下降法)
每次随机选取大小batch_size的子集进行批量训练
节省时间，更加准确
