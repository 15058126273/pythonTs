# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    time: 2017-02-10
    desc: 遍历三位数及以下域名是否 即将释放
"""
import requests
import json
import time
import os
import commonVariable

checkapi = commonVariable.checkapi
token = commonVariable.token
headers = commonVariable.headers
chartuple = commonVariable.chartuple

domainfile = os.path.join('file', 'savedays.txt')
currentfile = os.path.join('file', 'savedays_current.txt')

currentdigroup = [0]

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
                if code == 1 or code == 4:
                    print("域名未注册：", domain)
                    df = open(domainfile, 'r+')
                    df.seek(0, 2)
                    df.write(domain + '\n')
                    df.close()
                elif code == 0 or code == 5:
                    print("域名已注册或被预定：", domain)
                    cf = open(currentfile, 'w')
                    cf.write(str(currentdigroup))
                    cf.close()
                elif code == -3:
                    print("域名暂时不能注册：", domain)
                    cf = open(currentfile, 'w')
                    cf.write(str(currentdigroup))
                    cf.close()
                elif code == -1:
                    print("timeout:", domain)
                else:
                    print("未知code：", module, '>>>>>>>', domain)
            else:
                print('error>>>>>>>>>>>', jsonstr)
        else:
            print("请求失败：", res.status_code)
    except Exception as e:
        print("出错了", e)


def main():
    global currentdigroup
    if not os.path.exists(domainfile):
        df = open(domainfile, "w")
        df.close()
    if os.path.exists(currentfile):
        cf = open(currentfile, "r")
        i = cf.readline()
        if i:
            currentdigroup = eval(i)
    lens = len(chartuple)
    while len(currentdigroup) < 4:
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
    else:
        cf = open(currentfile, "w")
        cf.write('[0]')
        cf.close()

main()
