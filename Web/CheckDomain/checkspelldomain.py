# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    time: 2017-02-20
    desc: 整理有效的全拼域名
"""
import os

domainfilepath = os.path.join("file", "spelldomain.txt")
nicefilepath = os.path.join("file", "spell.txt")

spell1 = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'w', 'x', 'y', 'z']
spell2 = ['a', 'e', 'h', 'i', 'o', 'u']
spell3 = ['a', 'e', 'i', 'o', 'u', 'v', 'n', 'h']
spell4 = ['a', 'e', 'i', 'o', 'u', 'n', 'g']
spell5 = ['i', 'n', 'g']

def main():
    """
    获取所有域名 并 筛选
    """
    domains = collectdomain()
    print("得到", str(len(domains)), "个域名")
    if os.path.exists(nicefilepath):
        nicefile = open(nicefilepath, "r+")
        nicefile.seek(0)
        nicefile.truncate()
        nicefile.close()
    else:
        nicefile = open(nicefilepath, "w")
        nicefile.close()
    try:
        for line in domains:
            if '.com' in line:
                domain = line.split('.')[0]
                filtrate(domain)
            else: 
                pass
        else:
            print("完成")
    except Exception as e:
        print("出错了", e)


def collectdomain():
    """
    collect all domain and return
    """
    domains = []
    if os.path.exists(domainfilepath):
        domainfile = open(domainfilepath, "r")
        domains.extend(domainfile.readlines())
        domainfile.close()
    return domains


def filtrate(domain):
    """
    筛选域名
    """
    if domain:
        flag = False
        if countstr(domain) == 5:
            savedomain(domain)
            # length = countstr(domain)
            # if length != 0 and length <=3:
            #     flag = True
            # if flag:
            #     savedomain(domain)
        else:
            pass


def savedomain(domain):
    nicefile = open(nicefilepath, "r+")
    nicefile.seek(0, 2)
    nicefile.write(domain + ".com\n")
    nicefile.close()


def spelldomain(domain):
    """
    检测域名是否是拼音全拼
    """
    length = len(domain)
    if length >= 4:
        if domain[0] in spell1 and domain[1] in spell2 and domain[2] in spell3 and domain[3] in spell4:
            if length == 4 or (length == 5 and domain[4] in spell5):
                return True
    return False


def countstr(domain):
    """
    检测字符串中有多少不同字符
    """
    count = 0
    if domain:
        currenti = 0
        sl = len(domain)
        count = sl
        while currenti < sl -1:
            comparei = currenti + 1
            while comparei < sl:
                if domain[comparei] == domain[currenti]:
                    count -= 1
                    break
                comparei += 1
            currenti += 1
    return count


main()
