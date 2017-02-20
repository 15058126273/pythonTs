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
import requests


class CheckIp:
    def __init__(self, do_all, create_thread, url, contain, check_path, fail_path):
        # 客户端信息
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        # 是否要测试所有的ip（包括 之前失效的ip）
        self.All = do_all
        # 计划启动的线程数
        self.createThread = create_thread
        # 测试地址
        self.url = url
        # 匹配字符串
        self.contain = contain
        # 测试ip文件地址
        self.check_path = check_path
        # 失效ip文件地址
        self.fail_path = fail_path

        """******以下是内部变量*******"""
        # 要检测的ip
        self._check_ip = []
        # 失效的ip
        self._lines = []
        # 已检测的ip数
        self._checked = 0
        # 线程池
        self._threads = []
        # 测试通过的ip
        self._successIp = []
        # 测试未通过的ip
        self._deadIp = []
        # 已经结束的线程数
        self._doneNum = 0

        self._printnum = 0

    def run_check(self, check_file, fail_ip):
        self._check_ip_len = len(self._check_ip)
        while self._checked != self._check_ip_len:
            self._checked += 1
            self.checking(self._check_ip[self._checked-1], check_file)
        else:
            self._doneNum += 1
            self.catch_done(check_file, fail_ip)

    def checking(self, ip2, check_file):
        """
        代理连接测试
        :param ip2: 测试的代理ip
        :param check_file: 存放成功的代理ip文件
        :return:
        """
        ip2 = ip2.replace('\n', '')
        if ip2 in self._successIp or ip2 in self._deadIp:
            return
        else:
            req = urllib.request.Request(self.url)
            req.add_header('User-Agent', self.user_agent)
            socket.setdefaulttimeout(5)  # 超时未响应则为超时，跳过执行下一条
            try:
                msg = "..."
                # 添加代理
                proxy_handler = urllib.request.ProxyHandler({'http': ip2})
                proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
                opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
                # 添加头信息
                opener.addheaders = [
                    ('User-Agent', self.user_agent)
                ]
                response = opener.open(self.url)
                if response.status == 200:
                    data = response.read().decode()
                    if self.contain in data:
                        msg = "成功"
                        self._successIp.append(ip2)
                        check_file.seek(0, 2)
                        check_file.write(ip2+'\n')
                    else:
                        self._deadIp.append(ip2)
                        msg = "data信息不匹配"
                else:
                    self._deadIp.append(ip2)
                    msg = "status状态不正确："+response.status
            except Exception as e:
                self._deadIp.append(ip2)
                msg = "错误：" + str(e)[0:50]
        self._printnum += 1
        print(str(self._printnum), ':', str(self._check_ip_len), ip2, msg)

    def checking2(self, ip2, check_file):
        """
        代理连接测试
        :param ip2: 测试的代理ip
        :param check_file: 存放成功的代理ip文件
        :return:
        """
        ip2 = ip2.replace('\n', '')
        if ip2 in self._successIp or ip2 in self._deadIp:
            return
        socket.setdefaulttimeout(5)  # 超时未响应则为超时，跳过执行下一条
        msg = "成功"
        try:
            headers = {'User-Agent': self.user_agent}
            proxies = {"http": 'http://' + ip2 + '/', "https": 'http://' + ip2 + '/'}
            res = requests.get(self.url, params=None, headers=headers, proxies=proxies)
            if res.status_code == 200:
                self._successIp.append(ip2)
                check_file.seek(0, 1)
                check_file.write(ip2 + '\n')
            else:
                self._deadIp.append(ip2)
                msg = "错误："+str(res.status_code)
        except Exception as e:
            self._deadIp.append(ip2)
            msg = "错误："+str(e)[0:50]
        self._printnum += 1
        print(str(self._printnum), ':', str(len(self._check_ip)), ip2, msg)

    def catch_done(self, check_file, fail_ip):
        """
        线程结束时触发
        :return:
        """
        if self._doneNum == self.createThread:
            print('失效的ip数:', len(self._deadIp), '成功的ip数:', len(self._successIp))
            if len(self._deadIp):
                for ip1 in self._deadIp:
                    if ip1 not in self._lines:
                        self._lines.append(ip1)
                for ip1 in self._lines:
                    ip1 = ip1.replace('\n', '')
                    fail_ip.seek(0, 1)
                    fail_ip.write(ip1 + '\n')
            fail_ip.close()
            check_file.close()
            print('验证耗时：', math.floor(time.clock()), '秒')

    def start(self):
        # 要测试的ip文件
        check_file = open(self.check_path, 'r+')
        # 之前失效的ip文件
        fail_ip = open(self.fail_path, 'r+')
        self._check_ip = check_file.readlines()
        if self.All:
            for ip in fail_ip.readlines():
                self._check_ip.append(ip)
        else:
            self._lines = fail_ip.readlines()
        check_file.seek(0)
        check_file.truncate()
        fail_ip.seek(0)
        fail_ip.truncate()
        i = 0
        try:
            while i < self.createThread:
                conn = threading.Thread(target=self.run_check, args=[check_file, fail_ip])
                conn.start()
                self._threads.append(conn)
                i += 1
        finally:
            self.createThread = i


