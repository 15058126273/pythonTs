# -*- encoding=utf-8 -*-
"""
    python: 3.5
    author: yjy
    time: 2017-02-08
    desc: 整理有效的域名，找出一些自己想要的
"""
import os

dfpath = os.path.join("file", "save.txt")
sfpath = os.path.join("file", "nice.txt")

def main():
    """
    获取所有域名 并 筛选
    """
    df = open(dfpath, 'r')
    if os.path.exists(sfpath):
        sf = open(sfpath, "r+")
        sf.seek(0)
        sf.truncate()
        sf.close()
    else:
        sf = open(sfpath, "w")
        sf.close()
    try:
        line = df.readline()
        while line:
            if '.com' in line:
                domain = line.split('.')[0]
                filtrate(domain)
            else: 
                print('完')
            line = df.readline()
        else:
            print("完成")
    except Exception as e:
        print("出错了", e)
    finally:
        df.close()

def filtrate(domain):
    """
    筛选域名
    """
    if domain:
        flag = False
        length = countstr(domain)
        if length != 0 and length <=3:
            flag = True
        if flag:
            global first
            sf = open(sfpath, "r+")
            sf.seek(0, 2)
            sf.write(domain + ".com\n")
            sf.close()
        

def countstr(s):
    """
    检测字符串中有多少不同字符
    """
    count = 0
    if s:
        currenti = 0
        sl = len(s)
        count = sl
        while currenti < sl -1:
            comparei = currenti + 1
            while comparei < sl:
                if s[comparei] == s[currenti]:
                    count -= 1
                    break
                comparei += 1
            currenti += 1
    return count


main()
