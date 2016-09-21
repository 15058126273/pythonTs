# encoding=utf-8
# Python3.5
# 从文件中用正则匹配出所有代理ip并写入代理ip文件准备检测

import re

ip = []


def dispose_data(file_path):
    body = open(file_path, 'rb')
    line = body.readline()
    while line:
        res = re.search(r'>(([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3}))</td>', str(line))
        if res is not None:
            if res.group(1):
                host = res.group(1)
                line = body.readline()
                res = re.search(r'>([0-9]{1,5})</td>', str(line))
                port = res.group(1)
                ip.append(host+':'+port)
        line = body.readline()


def dispose_data2(file_path):
    body = open(file_path, 'rb')
    line = body.readline()
    while line:
        res = re.search(r'(([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3}):([0-9]{1,5}))@', str(line))
        if res is not None:
            if res.group(1):
                ip.append(res.group(1))
        line = body.readline()


def start(catch_path, save_path, mold):
    if mold == 1:
        dispose_data(catch_path)
    else:
        dispose_data2(catch_path)
    nowFile = open(save_path, 'r+')
    for i in ip:
        nowFile.seek(0, 2)
        nowFile.write(i+'\n')
    nowFile.close()


start('ipbody.txt', 'checkIp.txt', 2)
print('完成')
