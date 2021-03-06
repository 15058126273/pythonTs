# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    time: 2017-02-06
    desc: 遍历域名 查找 未注册的较短域名（效率低，易被屏蔽，改用 main_proxy.py）
"""
import requests
import json
import time
import os
import commonVariable
from os.path import join, exists

# 域名验证接口地址
checkapi = commonVariable.checkapi
# 接口提交必要参数
token = commonVariable.token
# headers
headers = commonVariable.headers
# 域名组成字符
chartuple = commonVariable.chartuple

# 未注册域名保存文件
domainfile = join('file','save.txt')
# 即将释放域名保存文件
predictedfile = join('file', 'predicted.txt')
# 当前域名检测进度保存
usedfile = join('file', 'current.txt')

# 初始域名
currentdigroup = [0]

# 检测域名的状态
def check(domain):
    try:
        url = checkapi + "?domain=" + domain + "&token=" + token + "&_" + str(time.time())
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.content.decode()
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
                    print("域名即将释放：", domain)
                    yf = open(predictedfile, 'r+')
                    yf.seek(0, 2)
                    yf.write(domain + '\n')
                    yf.close()
                elif code == 0 or code == 5:
                    print("域名已注册或被预定：", domain)
                elif code == -3:
                    print("域名暂时不能注册：", domain)
                elif code == -1:
                    print("timeout:", domain)
                else:
                    print("未知code：", module, '>>>>>>>', domain)
                df = open(usedfile, 'w')
                df.write(str(currentdigroup) + '\n')
                df.close()
            else:
                print('error>>>>>>>>>>>', jsonstr)
        else:
            print("请求失败：", res.status_code)
    except Exception as e:
        print("出错了", e)

# 主函数
def main():
    global currentdigroup
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
        check(domain+'.com')


if "__main__" == __name__:
    main()
