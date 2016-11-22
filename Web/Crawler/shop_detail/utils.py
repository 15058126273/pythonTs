# -*- encoding=utf-8 -*-
import re

class DescUtil:
	def __init__(self, opener):
		self.opener = opener

	def tbDescUrl(self, data):
		"""
		淘宝网详情图片抓取
		"""
		restr = re.compile(r'descUrl:location.protocol===\'http:\'\?\'(.*)\':')
		m = restr.search(data)
		if m and m.group():
			descUrl = m.group(1).replace("//","http://")
			self.catchDesc(descUrl)

	def tmDescUrl(self, data):
		"""
		天猫详情图片抓取
		"""
		restr = re.compile(r'descUrl\":\"(.*)\",\"fetchDcUrl')
		m = restr.search(data)
		if m and m.group(1):
			descUrl = m.group(1).replace("//", "http://")
			self.catchDesc(descUrl)

	def aliDescUrl(self, data):
		"""
		天猫详情图片抓取
		"""
		print(data)
		restr = re.compile(r'data-tfs-url=\"(.*)\"data-enable')
		m = restr.search(data)
		if m and m.group(1):
			descUrl = m.group(1)
			self.catchDesc(descUrl, mode='ali')


	def catchDesc(self, descUrl, mode=None):
		"""
		根据详情接口获取详情信息
		"""
		if descUrl:
			response = self.opener.open(descUrl)
			descData = response.read().decode("gbk")
			if mode == 'ali':
				restr = re.compile(r'var offer_details=(.*);')
				m2 = restr.search(descData)
				if m2 and m2.group(1):
					print(eval(m2.group(1))['content'])
			else:
				restr = re.compile(r'var desc=\'(.*)\';')
				m2 = restr.search(descData)
				if m2 and m2.group(1):
					print(m2.group(1))