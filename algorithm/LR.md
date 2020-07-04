# 回归算法 LR算法

二分类(Logistic Regression 逻辑斯谛回归 简称LR)：model -> 0/1

多分类(Softmax)：model -> 0/1/2...

## Sigmoid函数——逻辑回归的实现

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200628180453581.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

用sigmoid原因：简单来讲，可以将(-∞, +∞)的输入变量映射到(0,1)，作为后验概率

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200629104201740.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)

## Sigmoid函数输入

输入记为z=


## 举例：到达谷底的最佳路线

### 梯度

梯度方向-让f(x,y)函数快速变大的方向

反梯度方向-让f(x,y)函数快速变小的方向

### 实现

误差=真实值-预测值=(yi- 𝜂 (wxi))

errors = target - prediction

prediction=sigmoid(wx)=𝜂(wx)

wx=weight * x + b

### 对$\eta$求w偏导：
$\eta(t)=\frac{1}{1+e^{-t}}$ 转换为 $\eta(wx)=\frac{1}{1+e^{-wx}}$

偏导为$\frac{\partial(\eta)}{\partial(w)}$ $=\frac{(-1)}{(1+e^{-wx})^{2}} *(-x)*(e^{-wx}) $

$=\frac{1}{1+e^{-wx}} * \frac{e^{-wx}}{1+e^{-wx}} * x$

$=\frac{1}{1+e^{-wx}} * \frac{1+e^{-wx}-1}{1+e^{-wx}} * x$

$=\frac{1}{1+e^{-wx}} * (1 - \frac{1}{1+e^{-wx}}) * x$

$=\eta * (1-\eta) * x$

### 对损失函数$L(w)$求导（梯度）：

#### 类别概率
$p(y_{i}=1|x)=\eta$
$p(y_{i}=0|x)=1-\eta$

#### 似然函数
$L(w)=\prod\limits_{i}p(y_{i})$
$=\prod\limits_{i}(I(y_{i}=1)p(y_{i}=1|x_{i},w)) * I(y_{i}=0)p((y_{i}=0)|x_{i},w))$
$=\prod\limits_{i}y_{i}\eta * (1-y_{i})(1-\eta)$

#### 负对数似然
$log(L(w))=-log(\prod\limits_{i}y_{i}\eta * (1-y_{i})(1-\eta))$
$log(L(w))=-\sum\limits_{i}(y_{i}log(\eta)+(1-y_{i})log((1-\eta))$
 
#### 也有另一种表达式

$L(w)=-\sum\limits_{i}(I(y_{i}=1)log(p(y_{i}=1|x_{i},w))) + I(y_{i}=0)log(p((y_{i}=0)|x_{i},w)))$
$=-\sum\limits_{i}(I(y_{i}=1)log(\eta(wx_{i})) + I(y_{i}=0)log(1-\eta(wx_{i})))$

#### 所以负对数似然求偏导

$$\delta(L(w))=-\sum(\frac{y_{i}}{\eta}\eta(1-\eta)x_{i} - \frac{1-y_{i}}{1-\eta}\eta(1-\eta)x_{i})$$
$$=-\sum(y_{i}(1-\eta)x_{i}+(1-y_{i})\eta x_{i})$$
$$=-\sum(y_{i}x_{i}-y_{i}\eta  x_{i}-\eta x_{i}+y_{i}\eta x_{i})$$
$$=-\sum(y_{i}-\eta) x_{i}$$

$\nabla(L(w))=-\sum(y_{i}-\eta) x_{i}$


