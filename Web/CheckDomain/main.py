# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    time: 2017-02-06
    desc: 遍历域名 查找 未注册的较短域名
"""
import requests
import json
import time

checkapi = "https://checkapi.aliyun.com/check/checkdomain"
token = "check-web-hichina-com:1etx1glfwv32szgqu98ahei9wdxias4t"
headers = {
    'cookie': 'cna=0jW0ELoAp3YCATywgZSo5cVw; \
                aliyun_choice=CN; \
                aliyun_country=CN; \
                aliyun_site=CN; \
                _gat=1; \
                JSESSIONID=RM566QD1-3UMHA4Q0OZ9J6NYAGTBM1-AVG3VUYI-994X3; \
                tmp0=c8WhVh5Avk6gEEWwyjscNz9VvxWX7NRmDCS3yyTjWbjZ9h2e%2BQu%2Bf2JcHpu2nKjZ9CNxmaVgCot98zjkJamzy5Q%2FNMC3maLW%2BAWH6x%2Fm4GEqrzx12tN163mAfW8QDN0A3c2t%2BViwp87fa3kmjbyqQA%3D%3D; \
                l=Anh4lIvxdlpLty8AZJ2sujCqyCwK1txr; \
                isg=Arq60btRtqzGSDqq1DmqzVD8C-Di0z5Ff7C0rcSzUc0Yt1rxrfuOVYDNcdyL; \
                _ga=GA1.2.1402247830.1483939865',
    'pragma': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
}


def check(domain):
    try:
        url = checkapi + "?domain=" + domain + "&token=" + token + "&_" + str(time.time())
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.content.decode()
            jsonstr = json.loads(data)
            code = jsonstr.get("module")[0].get('avail')
            if code == 1:
                print("域名未注册：", domain)
                df = open(domainfile, 'r+')
                df.seek(0, 2)
                df.write(domain + '\n')
                df.close()
            elif code == 0:
                print("域名已注册：", domain)
                df = open(usedfile, 'w')
                df.write(str(currentdigroup) + '\n')
                df.close()
        else:
            print("请求失败：", res.status_code)
    except Exception as e:
        print("出错了", e)


domainfile = 'save.txt'
usedfile = 'used.txt'
chartuple = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
             'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
             'u', 'v', 'w', 'x', 'y', 'z')
cf = open(usedfile, 'r')
cstr = cf.readline()
currentdigroup = eval(cstr)
cf.close()
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
