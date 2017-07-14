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
import requests

# 检测域名状态接口
checkapi = commonVariable.checkapi
# 接口调用用到的token参数
token = ""
# 请求头headers
openheaders = commonVariable.openheaders
# 组装域名用到的字符集合
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
# 遍历进度
currentdigroup = [0]
# 线程池
threads = []
# 代理ip文件地址
proxyipfilepath = os.path.join("file", "proxyIp.txt")
# 代理ip数组
proxyips = []
# 代理ip的数量
ipcount = len(proxyips) - 1
# 程序是否正在运行中...
running = False


def main():
    """
    主程序入口
    """
    global proxyips, currentdigroup, threads, fileindex, running, \
        domainfilepath, fileindexpath, usedfilepath, predictedfilepath
    # 获取代理ip列表
    proxyipfile = open(proxyipfilepath, "r")
    proxyips = proxyipfile.readlines()
    proxyipfile.close()
    # 下标保存
    if not os.path.exists(fileindexpath):
        fc = open(fileindexpath, "w")
        fc.write("0")
        fc.close()
    else:
        fc = open(fileindexpath, "r")
        istr = fc.readline()
        fileindex = int(istr)
        fc.close()
    # 遍历进度保存
    if os.path.exists(usedfilepath):
        cf = open(usedfilepath, 'r')
        try:
            cstr = cf.readline()
            if cstr != "":
                currentdigroup = eval(cstr)
        finally:
            cf.close()
    # 有效域名保存
    if not os.path.exists(domainfilepath.replace('INDEX', str(fileindex))):
        domainfile = open(domainfilepath.replace('INDEX', str(fileindex)), "w")
        domainfile.close()
    # 待释放域名保存
    if not os.path.exists(predictedfilepath):
        predictedfile = open(predictedfilepath, "w")
        predictedfile.close()
    # 域名 待试用字符
    lens = len(chartuple)
    i = 0
    try:
        print("创建进度监听线程..")
        filecontrol = threading.Thread(target=checkprocess, args=[])
        filecontrol.start()
        print("创建进度监听线程成功...")
        print("创建主程序线程....")
        while i < 10:
            conn = threading.Thread(target=threadsons, args=[lens])
            conn.start()
            threads.append(conn)
            i += 1
    finally:
        print("成功创建", i, "个主程序线程....")
        running = True

# 获取token
def gettoken():
    # token = "check-web-hichina-com:wzgm5ktpim76go3ut3mufcht749jk14q"
    xv = "0.8.1"
    xa = "check-web-hichina-com"
    token_temp = xa + ":" + generateToken()
    xh = ""
    x0 = "-^^-^^-^^-^^-^^-^^-^^-^^-^^-^^-^^-^^-^^-"
    x1 = "1^^-^^-^^-^^-^^-^^-^^-^^-^^-^^-^^-^^-^^Win32"
    x2 = "Mozilla^^-^^Netscape^^5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36^^-^^-^^-^^-^^-^^-^^Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36^^-^^-"
    x3 = "1040^^1920^^21^^804^^1080^^zh-CN^^http%3A%2F%2Flocalhost%3A63343%2FWebStormSpace%2Ftest_html%2FaliDomain.html^^-^^-^^-^^1500006621441^^480^^1920"
    xs = "55F3A8BFC9C50DDA7783BC1EA71631DAC940CCEF69ED67FE38FD999804E3ED39FCB31B6BD58596D5CD43AD3E795C914C8A6A5BA03F3FD2E28D3A60914E86D4A7"
    api = "https://ynuf.alipay.com/service/um.json?xv=" + xv + "&xa=" + xa + "&xt=" + token_temp + "&xh=" + xh + "&x0=" + x0 + "&x1=" + x1 + "&x2=" + x2 + "&x3=" + x3 + "&xs=" + xs
    res = requests.get(api)
    if (res.status_code == 200):
        print("获取token成功：" + token_temp)
    return token_temp


# 生成一个随机的token
def generateToken():
    data = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    result = []
    length = len(data);
    for c in range(32):
        result.append(data[math.floor(random.random() * length)])
    return "".join(result)

def checkdomain(domain, flag):
    """
    检测域名的状态
    :param domain: 域名
    :param flag: 访问接口失败后是否重新调用
    :return:
    """
    token = gettoken()
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
                    print("域名即将释放：", domain)
                    predictedfile = open(predictedfilepath, 'r+')
                    predictedfile.seek(0, 2)
                    predictedfile.write(domain + '\n')
                    predictedfile.close()
                elif code == 0 or code == 5:
                    pass
                    print("已注册或预定：", domain)
                elif code == -3:
                    pass
                    print("域名暂时不能注册：", domain)
                elif code == -1:
                    pass
                    print("timeout:", domain)
                else:
                    print("未知code：", module, '>>>>>>>', domain)
            else:
                if flag:
                    checkdomain(domain, False)
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
    """
    数字与字母组合
    :param lens: 字符集合大小
    :return:
    """
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
    :return:
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
            time.sleep(2)
        





if "__main__" == __name__:
    main()
