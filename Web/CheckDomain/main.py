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
token = "check-web-hichina-com%3A586su69u61skrvkdcyo3tq1ob8tuhmgx"
headers = {
    'cookie': 'cna=a0W1EHToizQCAXPNbSnPjg7N; \
                aliyun_choice=CN; industry-tip=true; activeRegionId=cn-hangzhou; \
                login_aliyunid="aly_niuss00****"; \
                login_aliyunid_ticket=fyKpeu*0vCmV8s*MT5tJl3_1$$wSmWz4wUh_yrieFJ*hxv4OmpI67sQZD5G2agBdxkJCqf_kNpoU_BOTwChTBoNM1ZJeedfK9zxYnbN5hossqIZCr6t7SGxRigm2Cb4fGaCdBZWIzmgdHq6sXXZQg4WF0; \
                login_aliyunid_csrf=_csrf_tk_1007686368281536; \
                login_aliyunid_pk=1855560471338865; \
                hssid=1JpvygSHfHve3M0wP7KHmIA1; \
                hsite=6; \
                aliyun_country=CN; \
                aliyun_site=CN; \
                sidebar-type=full; \
                consoleRecentVisit=ocs%2Cecs%2Cslb; \
                JSESSIONID=Y0666R81-YTMHRTRWSY5RP1ZRSJJU1-2C4ZUTYI-NR4Q3; \
                tmp0=c8WhVh5Avk6gEEWwyjscN7z6D%2BRR1MtQeF3ZAyZW3WLXRxButCkV6z9DCyb6kSbZo1IjcYQ%2B1B%2B%2B5F3Ei43wOK0Mdy%2FOF2L1IDH8kPMpHC3Yyi8L06tsfz15fLHhaHACTyv29I17yOjByppv0cb0AQ%3D%3D; \
                _ga=GA1.2.1187146787.1479694972; \
                l=Avr/9rRghokQa-gncUMOZbT/yipZf36d; \
                isg=AoqKYZsX5l0M92UVPjYmq2iM23DwIA7VSsHHWRSG4l1wx7aBlQhX5Rd1oYTh',
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
            print(data)
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
        else:
            print("请求失败：", res.status_code)
    except Exception as e:
        print("出错了", e)


domainfile = 'save.txt'
chartuple = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
             'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
             'u', 'v', 'w', 'x', 'y', 'z')
currentdigroup = [0, 15, 19]
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
