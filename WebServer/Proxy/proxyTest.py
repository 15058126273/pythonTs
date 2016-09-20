#! /usr/bin/env python3
# -*- coding:utf-8 -*-
#

import urllib.request
import urllib.parse
import socket

readyIp = [
        '212.83.166.180:8080'
            ]

successIp = []
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
        socket.setdefaulttimeout(5)  # 3秒未响应则为超时，跳过执行下一条
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
            successIp.append(ip)
            print(ip, "正确：" + str(response_data))
        except Exception as e:
            deadIp.append(ip)
            print(ip, "错误：", e)

cu = curl()
for ip in readyIp:
    cu.run("http://cn-proxy.com/", ip)

print('失效的ip数:', len(deadIp))
print('成功的ip数:', str(successIp))

# cu = curl()
# cu.run('http://www.langsspt.com/', '210.13.73.133:8080')