二分类(LR)：model -> 0/1
多分类(Softmax)：model -> 0/1/2...

评估方式：PR曲线——确定阈值（人工设定）

sifmoid函数——逻辑回归的实现
                1
𝜂(𝑡)=-------------
          1+exp(-t)

负对数似然：
	L(w) = - Σ(I(yi=0)log(p(yi=1|xi,w))+ I(yi=0) log(p(yi=0|xi,w)))
	=- Σ(I(yi=1)log(𝜂(wxi)) +I(yi=0)log(1-𝜂(wxi)))

I(x):符号函数
  x条件成立=1
  x条件不成立 != 1

梯度：
	𝛻L(w)=-Σ(yi-𝜂(wxi))xi

f(x) = sigmoid(wx)
w1：随机初始化——》f(x) ：预测值