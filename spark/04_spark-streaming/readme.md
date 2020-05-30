
- 1.运行任务

1>标准输出 2>错误输出

bash wc_local.sh 1>1.log 2>2.log

- 2.监控日志

tail -f 1.log

- 3.打开端口

nc -l 9999


- 4.测试wordCount

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200530190052382.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0FsYmVydExpYW5nenQ=,size_16,color_FFFFFF,t_70)