# -*- encoding=utf-8 -*-
"""
	python: 3.5
	author: yjy
	time: 2016-11-25
	desc: 抓取淘宝天猫阿里巴巴京东平台的宝贝详情
"""
import urllib.request
import re
import utils

proxy_handler = urllib.request.ProxyHandler(None)
proxy_auth_handler = urllib.request.ProxyBasicAuthHandler
opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)

util = utils.DescUtil(opener)

def catchUrl(url, mode):
	"""
	根据宝贝链接和平台获取宝贝详情（mode:1 淘宝   2 天猫  3 阿里巴巴）
	"""
	response = opener.open(url)
	data = response.read().decode("gbk").replace(" ", "")
	if mode == 1:
		util.tbDescUrl(data)
	elif mode == 2:
		util.tmDescUrl(data)
	elif mode == 3:
		util.aliDescUrl(data)

def jdDesc(id):
	"""
	根据id获取京东宝贝详情
	"""
	descUrl = 'https://dx.3.cn/desc/'+str(id)
	response = opener.open(descUrl)
	data = response.read().decode('gbk')
	data = data.replace("showdesc", "").replace("//","http://").replace("data-lazyload", "src")
	print(data)
	content = eval(data)['content']
	print(content)

# jdDesc(1190252)
catchUrl("https://item.taobao.com/item.htm?spm=a230r.1.14.20.fIPhTs&id=522536975247&ns=1&abbucket=11#detail", 1)
