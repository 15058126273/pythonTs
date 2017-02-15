# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    time: 2017-02-15
    desc: 遍历域名 查找 未注册的较短域名 (使用代理ip)
"""
import requests
import json
import time
import os
import tokenCode
import random
import math
import threading
import urllib.parse
import urllib.request
import socket
import re

checkapi = tokenCode.checkapi
token = tokenCode.token
headers = tokenCode.headers

domainfile = 'save.txt'
predictedfile = 'predicted.txt'
usedfile = 'current2.txt'
chartuple = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
             'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
             'u', 'v', 'w', 'x', 'y', 'z')
currentdigroup = [0, 0, 0, 0]
threads = []
createThread = 0
proxyipfile = open("checkIp.txt", "r")
proxyips = proxyipfile.readlines()
ipcount = len(proxyips) - 1

def check(domain, flag):
    try:
        url = checkapi + "?domain=" + domain + "&token=" + token + "&_" + str(time.time())
        # 添加代理
        ip = proxyips[math.floor(random.random()*ipcount)]
        proxy_handler = urllib.request.ProxyHandler({'http': ip})
        proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
        opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
        # 添加头信息
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
        ]
        res = opener.open(url)
        if res.status == 200:
            data = res.read().decode()
            jsonstr = json.loads(data)
            if jsonstr.get("errorCode") == 0:
                module = jsonstr.get("module")[0]
                code = module.get("avail")
                if code == 1:
                    print("域名未注册：", domain)
                    df = open(domainfile, 'r+')
                    df.seek(0, 2)
                    df.write(domain + '\n')
                    df.close()
                elif code == 4:
                    # print("域名即将释放：", domain)
                    yf = open(predictedfile, 'r+')
                    yf.seek(0, 2)
                    yf.write(domain + '\n')
                    yf.close()
                elif code == 0 or code == 5:
                    pass
                    # print("已注册或预定：", domain)
                elif code == -3:
                    pass
                    # print("域名暂时不能注册：", domain)
                elif code == -1:
                    pass
                    # print("timeout:", domain)
                else:
                    print("未知code：", module, '>>>>>>>', domain)
                df = open(usedfile, 'w')
                df.write(str(currentdigroup) + '\n')
                df.close()
            else:
                print('error>>>>>>>>>>>', jsonstr)
        else:
            print("请求失败：", res.status)
            if flag:
                check(domain, False)
    except Exception as e:
        print("出错了", e)
        if flag:
            check(domain, False)


def threadsons(lens):
    global currentdigroup
    while 1:
        changei = len(currentdigroup) - 1
        while currentdigroup[changei] == lens - 1:
            currentdigroup[changei] = 0
            changei -= 1
            if changei < 0:
                break
        if changei < 0:
            changei = 0
            while changei < len(currentdigroup) - 1:
                changei += 1
                currentdigroup[changei] = 0
            currentdigroup.append(0)
        else:
            currentdigroup[changei] += 1
        domain = ''
        i = 0
        while i < len(currentdigroup):
            domain += chartuple[currentdigroup[i]]
            i += 1
        check(domain+'.com', True)

def main():
    global currentdigroup, threads, createThread
    if os.path.exists(usedfile):
        cf = open(usedfile, 'r')
        cstr = cf.readline()
        currentdigroup = eval(cstr)
        cf.close()
    if not os.path.exists(domainfile):
        df = open(domainfile, "w")
        df.close()
    if not os.path.exists(predictedfile):
        yf = open(predictedfile, "w")
        yf.close()
    lens = len(chartuple)
    i = 0
    try:
        while i < 100:
            conn = threading.Thread(target=threadsons, args=[lens])
            conn.start()
            threads.append(conn)
            i += 1
    finally:
        createThread = i
        print("成功创建", i, "个线程")


main()
