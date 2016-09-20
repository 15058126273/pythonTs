# -*- encoding=utf-8 -*-
# Python 3.5  2016-09-20
# 代理ip检测

import urllib.request
import urllib.parse
import socket
import threading
import math

_author = 'yjy'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
             (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
# 测试通过的ip
successIp = []
# 测试未通过的ip
deadIp = []
# 已经结束的线程数
doneNum = 0
# 计划启动的线程数
createThread = 20
# 测试地址
url = "http://www.langsspt.com/"
# 要测试的ip文件
check_file = open('proxyIp.txt', 'r+')
# 之前失效的ip文件
fail_ip = open('failip.txt', 'r+')
# 是否要测试所有的ip（包括 之前失效的ip）
All = True
# 当次运行需要测试的ip
check_ip = check_file.readlines()
# 失效的ip
lines = []
# 已检测的ip数
checked = 0
# 线程池
threads = []


def run_check():
    global doneNum, checked
    while checked != len(check_ip):
        checked += 1
        checking(check_ip[checked-1])
    else:
        doneNum += 1
        catch_done()


def checking(ip2):
    """
    代理连接测试
    :param ip2: 测试的代理ip
    :return:
    """
    ip2 = ip2.replace('\n', '')
    if ip2 in successIp or ip2 in deadIp:
        return
    req = urllib.request.Request(url)
    req.add_header('User-Agent', user_agent)
    socket.setdefaulttimeout(5)  # 3秒未响应则为超时，跳过执行下一条
    try:
        # 添加代理
        proxy_handler = urllib.request.ProxyHandler({'http': ip2})
        proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
        opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
        # 添加头信息
        opener.addheaders = [
            ('User-Agent', user_agent)
        ]
        response = opener.open(url)
        data = response.read()
        successIp.append(ip2)
        check_file.seek(0, 1)
        check_file.write(ip2+'\n')
        print(ip2, "成功")
    except Exception as e:
        deadIp.append(ip2)
        print(ip2, "错误：", e)


def catch_done():
    """
    线程结束时触发
    :return:
    """
    if doneNum == createThread:
        print('失效的ip数:', len(deadIp), '成功的ip数:', len(successIp))
        if len(deadIp):
            for ip1 in deadIp:
                if ip1 not in lines:
                    lines.append(ip1)
            for ip1 in lines:
                ip1 = ip1.replace('\n', '')
                fail_ip.seek(0, 1)
                fail_ip.write(ip1 + '\n')
        fail_ip.close()
        check_file.close()


def start():
    """
    开始函数
    """
    global createThread, lines
    if All:
        for ip in fail_ip.readlines():
            check_ip.append(ip)
    else:
        lines = fail_ip.readlines()
    check_file.seek(0)
    check_file.truncate()
    fail_ip.seek(0)
    fail_ip.truncate()
    i = 0
    try:
        while i < createThread:
            conn = threading.Thread(target=run_check)
            conn.start()
            threads.append(conn)
            i += 1
    finally:
        createThread = i


start()
