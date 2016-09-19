#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import urllib.request
import urllib.parse
import socket

readyIp = [
            '111.12.251.169:80',
            '111.12.251.172:80',
            '111.12.251.173:80',
            '111.12.251.174:80',
            '111.12.251.207:80',
            '111.12.251.213:80',
            '117.135.250.133:80',
            '117.135.250.134:80',
            '120.192.92.98:80',
            '183.245.146.62:80',
            '211.143.146.231:80',
            '221.130.13.238:80'
            ]

deadIp = []

class curl:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
                            (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        self.proxyIpList = ['119.88.128.77:80']

    # 进行数据提交
    def run(self, url, ip):
        # data = urllib.parse.urlencode(self.param).encode(encoding='UTF8');
        req = urllib.request.Request(url)
        req.add_header('User-Agent', self.user_agent)
        socket.setdefaulttimeout(10)  # 3秒未响应则为超时，跳过执行下一条
        try:
            # 添加代理
            proxy_handler = urllib.request.ProxyHandler({'http': ip})
            proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
            opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
            # 添加头信息
            opener.addheaders = [
                ('User-Agent', self.user_agent)
            ]
            # 数据请求
            response = opener.open(url)
            # 获取请求返还数据
            response_data = response.read()
            print(ip, "正确：" + str(response_data))
        except Exception as e:
            deadIp.append(ip)
            print(ip, "错误：", e)

cu = curl()
for ip in readyIp:
    cu.run("http://www.langsspt.com/", ip)

print('失效的ip数:', len(deadIp))

# cu = curl()
# cu.run('http://www.langsspt.com/', '210.13.73.133:8080')