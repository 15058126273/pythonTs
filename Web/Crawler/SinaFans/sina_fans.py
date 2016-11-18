# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    time: 2016-11-18
    desc: 抓取新浪微博所有用戶的粉丝数
"""
import requests
import re
import socket


class SinaFans:
    def __init__(self):
        self.headers = {
            "Cookie": "YF-Ugrow-G0=3a02f95fa8b3c9dc73c74bc9f2ca4fc6; \
            SUB=_2AkMvck_vf8NhqwJRmP4UymLibox3zwzEieLBAH7sJRMxHRl-yT83qn0StRBHsQfwSfDmhx2jCrwvYqn_oUwvPQ..; \
            SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFe7ir_.E1hmCsrzF76ZV7c; \
            login_sid_t=2011850be0affbbcf60024c2dc53a088; \
            YF-V5-G0=16139189c1dbd74e7d073bc6ebfa4935; \
            WBStorage=2c466cc84b6dda21|undefined; \
            YF-Page-G0=e1a5a1aae05361d646241e28c550f987; _s_tentry=-; \
            Apache=2637200928293.1685.1479459032669; \
            SINAGLOBAL=2637200928293.1685.1479459032669; \
            ULV=1479459032712:1:1:1:2637200928293.1685.1479459032669:"
        }

    def catch_sb(self, id):
        socket.setdefaulttimeout(5)
        param = {'ajwvr': 6, 'id': id, 'type': 1}
        res = requests.get("http://weibo.com/aj/v6/user/newcard", params=param, headers=self.headers)
        print(res.status_code)
        if res.status_code == 200:
            data = res.text
            regexpr = re.compile(r'&nick=(.*)\\\" suda-uatrack=\\\"key=(.*)&value=privateletter\\\">', re.DOTALL)
            regexpr2 = re.compile(r'class=\\\"num W_fb\\\">(.*)<\\/em><\\/a><\\/span>\\n        <span', re.DOTALL)
            m = regexpr.search(data)
            m2 = regexpr2.search(data)
            if m and m2:
                fans = m2.group(1).encode().decode("unicode-escape")
                fans = fans.replace("万", '0000')
                print(m.group(1).encode().decode("unicode-escape"), "：", int(fans))
            else:
                print("获取用户",id,"的信息时失败")
        else:
            print("读取失败：" + res.status_code)

if "__main__" == __name__:
    sina = SinaFans()
    id = 3
    allid = 10000000000
    while id < allid:
        try:
            sina.catch_sb(id)
        except Exception as e:
            print("获取用户",id,"的信息时出错:",e)
        id += 1
