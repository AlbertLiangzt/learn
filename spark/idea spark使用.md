## 添加scala类（右键New无scala选项）

选中项目 > 右键 > AddFrameworkSupport... > 选中Scala > 选择scala版本

创建scala文件，选择Object

## 压缩包

选中项目>右键>Open Module Settings>Artifacts>Jar>From  Modules with >dependence

## 在Windows下打包
1.编译Build > Build Artifacts... > Build

2.打包在maven选项栏中 > install

jar包生成路径，在对应的/target/***.jar

注意，如果之前有jar包，需要先删除，不然不会覆盖


## 在linux下打包
1.直接在maven选项栏中 > install