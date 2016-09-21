# -*- encoding=utf-8 -*-
"""
    Python 3.5
    2016-09-20
    author = yjy
    代理ip检测
"""
import urllib.request
import urllib.parse
import socket
import threading
import math
import time


class CheckIp:
    def __init__(self):
        # 客户端信息
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        # 是否要测试所有的ip（包括 之前失效的ip）
        self.All = False
        # 计划启动的线程数
        self.createThread = 40
        # 测试地址
        self.url = "http://www.langsspt.com/"
        # 测试ip文件地址
        self.check_path = 'checkIp.txt'
        # 失效ip文件地址
        self.fail_path = 'failip.txt'

        """******以下是内部变量*******"""
        # 要检测的ip
        self.check_ip = []
        # 失效的ip
        self.lines = []
        # 已检测的ip数
        self.checked = 0
        # 线程池
        self.threads = []
        # 测试通过的ip
        self.successIp = []
        # 测试未通过的ip
        self.deadIp = []
        # 已经结束的线程数
        self.doneNum = 0

    def run_check(self, check_file, fail_ip):
        while self.checked != len(self.check_ip):
            self.checked += 1
            self.checking(self.check_ip[self.checked-1], check_file)
        else:
            self.doneNum += 1
            self.catch_done(check_file, fail_ip)

    def checking(self, ip2, check_file):
        """
        代理连接测试
        :param ip2: 测试的代理ip
        :param check_file: 存放成功的代理ip文件
        :return:
        """
        ip2 = ip2.replace('\n', '')
        if ip2 in self.successIp or ip2 in self.deadIp:
            return
        req = urllib.request.Request(self.url)
        req.add_header('User-Agent', self.user_agent)
        socket.setdefaulttimeout(5)  # 超时未响应则为超时，跳过执行下一条
        try:
            # 添加代理
            proxy_handler = urllib.request.ProxyHandler({'http': ip2})
            proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
            opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
            # 添加头信息
            opener.addheaders = [
                ('User-Agent', self.user_agent)
            ]
            opener.open(self.url)
            # response = opener.open(self.url)
            # data = response.read()
            self.successIp.append(ip2)
            check_file.seek(0, 1)
            check_file.write(ip2+'\n')
            print(ip2, "成功")
        except Exception as e:
            self.deadIp.append(ip2)
            print(ip2, "错误：", e)

    def catch_done(self, check_file, fail_ip):
        """
        线程结束时触发
        :return:
        """
        if self.doneNum == self.createThread:
            print('失效的ip数:', len(self.deadIp), '成功的ip数:', len(self.successIp))
            if len(self.deadIp):
                for ip1 in self.deadIp:
                    if ip1 not in self.lines:
                        self.lines.append(ip1)
                for ip1 in self.lines:
                    ip1 = ip1.replace('\n', '')
                    fail_ip.seek(0, 1)
                    fail_ip.write(ip1 + '\n')
            fail_ip.close()
            check_file.close()
            print('验证耗时：', math.floor(time.clock()), '秒')

    def start(self):
        time.clock()
        # 要测试的ip文件
        check_file = open(self.check_path, 'r+')
        # 之前失效的ip文件
        fail_ip = open(self.fail_path, 'r+')
        self.check_ip = check_file.readlines()
        if self.All:
            for ip in fail_ip.readlines():
                self.check_ip.append(ip)
        else:
            self.lines = fail_ip.readlines()
        print(self.check_ip)
        check_file.seek(0)
        check_file.truncate()
        fail_ip.seek(0)
        fail_ip.truncate()
        i = 0
        try:
            while i < self.createThread:
                conn = threading.Thread(target=self.run_check, args=[check_file, fail_ip])
                conn.start()
                self.threads.append(conn)
                i += 1
        finally:
            self.createThread = i


