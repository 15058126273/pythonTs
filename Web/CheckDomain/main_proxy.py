# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    time: 2017-02-15
    desc: 遍历域名 查找 未注册的较短域名 (使用代理ip)
"""
import json
import time
import os
import commonVariable
import random
import math
import threading
import urllib.parse
import urllib.request

checkapi = commonVariable.checkapi
token = commonVariable.token
openheaders = commonVariable.openheaders
chartuple = commonVariable.chartuple

# 指定保存的文件名与地址
domainfilepath = os.path.join('file', 'save_INDEX.txt')
# 保存文件的序号 初始序号0
fileindex = 0
# 保存文件序号的保存地址
fileindexpath = os.path.join('file', 'file_index.txt')
# 即将释放域名的保存地址
predictedfilepath = os.path.join('file', 'predicted.txt')
# 遍历进度的保存地址
usedfilepath = os.path.join('file', 'current.txt')


currentdigroup = [0, 0, 0, 0]
threads = []
proxyipfile = open(os.path.join("file", "proxyIp.txt"), "r")
proxyips = proxyipfile.readlines()
ipcount = len(proxyips) - 1
running = False


def checkdomain(domain, flag):
    url = checkapi + "?domain=" + domain + "&token=" + token + "&_" + str(time.time())
    # 添加代理
    ip = proxyips[math.floor(random.random()*ipcount)]
    proxy_handler = urllib.request.ProxyHandler({'http': ip})
    proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
    opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
    # 添加头信息
    opener.addheaders = openheaders
    try:
        res = opener.open(url)
        if res.status == 200:
            data = res.read().decode()
            jsonstr = json.loads(data)
            if jsonstr.get("errorCode") == 0:
                module = jsonstr.get("module")[0]
                code = module.get("avail")
                if code == 1:
                    # print(domain)
                    domainfile = open(domainfilepath.replace("INDEX", str(fileindex)), 'r+')
                    domainfile.seek(0, 2)
                    domainfile.write(domain + '\n')
                    domainfile.close()
                elif code == 4:
                    # print("域名即将释放：", domain)
                    predictedfile = open(predictedfilepath, 'r+')
                    predictedfile.seek(0, 2)
                    predictedfile.write(domain + '\n')
                    predictedfile.close()
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
            else:
                print('error>>>>>>>>>>>', jsonstr)
        else:
            if flag:
                checkdomain(domain, False)
            else:
                print("请求失败：", res.status)
    except Exception as e:
        if flag:
            checkdomain(domain, False)
        else:
            print("出错了", e)


def threadsons(lens):
    global currentdigroup
    while True:
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
        checkdomain(domain+'.com', True)


def checkprocess():
    """
    1、检测文件大小,如果文件大小超过1M则新建文件
    2、记录遍历进度
    """
    global fileindex, domainfilepath, fileindexpath, running
    while True:
        if running:
            filepath = domainfilepath.replace('INDEX', str(fileindex))
            s = os.path.getsize(filepath) / 1024 / 1024
            if s > 1:
                # 新建文件
                newfilepath = domainfilepath.replace('INDEX', str(fileindex + 1))
                newfile = open(newfilepath, "w")
                newfile.close()
                fileindex += 1
                fileindexfile = open(fileindexpath, "w")
                fileindexfile.write(str(fileindex))
                fileindexfile.close()
            # 记录遍历进度
            groupstr = str(currentdigroup)
            print("当前遍历进度：", groupstr)
            usedfile = open(usedfilepath, 'w')
            usedfile.write(groupstr)
            usedfile.close()
            # 休息几秒
            time.sleep(3)
        

def main():
    global currentdigroup, threads, fileindex, running, \
        domainfilepath, fileindexpath, usedfilepath, predictedfilepath
    if not os.path.exists(fileindexpath):
        fc = open(fileindexpath, "w")
        fc.write("0")
        fc.close()
    else:
        fc = open(fileindexpath, "r")
        istr = fc.readline()
        fileindex = int(istr)
        fc.close()
    if os.path.exists(usedfilepath):
        cf = open(usedfilepath, 'r')
        cstr = cf.readline()
        currentdigroup = eval(cstr)
        cf.close()
    if not os.path.exists(domainfilepath.replace('INDEX', str(fileindex))):
        domainfile = open(domainfilepath.replace('INDEX', str(fileindex)), "w")
        domainfile.close()
    if not os.path.exists(predictedfilepath):
        predictedfile = open(predictedfilepath, "w")
        predictedfile.close()
    lens = len(chartuple)
    i = 0
    try:
        print("创建进度监听线程..")
        filecontrol = threading.Thread(target=checkprocess, args=[])
        filecontrol.start()
        print("创建进度监听线程成功...")
        print("创建主程序线程....")
        while i < 200:
            conn = threading.Thread(target=threadsons, args=[lens])
            conn.start()
            threads.append(conn)
            i += 1
    finally:
        print("成功创建", i, "个主程序线程....")
        running = True


if "__main__" == __name__:
    main()
