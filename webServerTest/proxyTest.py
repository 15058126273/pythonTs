#! /usr/bin/env python3
# -*- coding:utf-8 -*-

'python进行代理的curl数据提交'

__author__ = 'ken'

import os;
import sys;

curPath = os.path.abspath(os.path.dirname(__file__));
sys.path.append(curPath);

import urllib.request;
import urllib.parse;
import socket;


class curl:
    def __init__(self):
        pass;

    # 获取用户浏览器信息
    def getUserAgent(self):
        userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0';
        return userAgent

    # 进行数据提交
    def run(self, url):
        self.url = url
        self.userAgent = self.getUserAgent()
        self.proxyIpList = ['124.240.187.78:81'];

        # data = urllib.parse.urlencode(self.param).encode(encoding='UTF8');
        req = urllib.request.Request(self.url)
        req.add_header('User-Agent', self.userAgent)

        for proxyIp in self.proxyIpList:
            socket.setdefaulttimeout(30)  # 3秒未响应则为超时，跳过执行下一条
            try:
                # 添加代理
                proxy_handler = urllib.request.ProxyHandler({'http': proxyIp})
                proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
                opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)

                # 添加头信息
                opener.addheaders = [
                    ('User-Agent', self.userAgent)
                ]

                # 数据请求
                response = opener.open(self.url)
                # 获取请求返还数据
                response_data = response.read()
                print(proxyIp, "正确：" + str(response_data))
                # return response_data;
            except urllib.error.HTTPError as e:
                print(proxyIp, "错误：", e)
                # print("错误内容：", e.read().decode("utf8"));
            except urllib.error.URLError as e:
                print(proxyIp, '错误：未能获取服务器信息.',e)
                # print('错误原因: ', e.reason);
            except Exception as e:
                print(proxyIp, "错误：其他未知错误！",e)

cu = curl()
cu.run("http://www.yangqq.com/")