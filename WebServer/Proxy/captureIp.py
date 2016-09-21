# -*- encoding=utf-8 -*-
"""
    Python 3.5
    2016-09-21
    author = yjy
"""
import urllib.parse
import urllib.request
import socket
import re


class CaptureIp:
    def __init__(self):
        self.url = 'http://www.kuaidaili.com/free/inha/'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        self.file_path = 'ipbody.txt'
        self.save_path = 'checkIp.txt'
        self.got_ip = []
        # 是否验证抓取到的ip
        self.need_verify = True
        # 起始页号
        self.page = 1
        # 抓取页数
        self.pages = 10

    def http_conn(self, page):
        req = urllib.request.Request(self.url)
        req.add_header('User-Agent', self.user_agent)
        socket.setdefaulttimeout(5)  # 3秒未响应则为超时，跳过执行下一条
        try:
            # 添加代理
            opener = urllib.request.build_opener()
            # 添加头信息
            opener.addheaders = [
                ('User-Agent', self.user_agent)
            ]
            response = opener.open(self.url+str(page)+'/')
            data = response.read()
            ipbody = open(self.file_path, 'rb+')
            ipbody.seek(0)
            ipbody.truncate()
            ipbody.write(data)
            ipbody.close()
            self.check_collect()
        except Exception as e:
            print("错误：", e)

    def dispose_data(self):
        body = open(self.file_path, 'rb')
        line = body.readline()
        while line:
            res = re.search(r'>(([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3}))</td>', str(line))
            if res is not None:
                if res.group(1):
                    host = res.group(1)
                    line = body.readline()
                    res = re.search(r'>([0-9]{1,5})</td>', str(line))
                    port = res.group(1)
                    self.got_ip.append(host+':'+port)
            line = body.readline()
        body.close()

    def check_collect(self):
        self.dispose_data()
        nowFile = open(self.save_path, 'r+')
        for i in self.got_ip:
            nowFile.seek(0, 2)
            nowFile.write(i+'\n')
        nowFile.close()

    def start(self):
        i = self.page
        while i <= self.pages:
            print('正在抓取第', i, '页，共', self.pages, '页')
            self.http_conn(i)
            i += 1
        else:
            print('抓取完成')

