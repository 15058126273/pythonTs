# encoding=utf-8
# Python3.5
# 从文件中用正则匹配出所有代理ip并写入代理ip文件准备检测

import re

ip = []


def dispose_data(file_path):
    body = open(file_path, 'rb')
    line = body.readline()
    while line:
        res = re.search(r'<td>((.*)\.(.*)\.(.*)\.(.*))</td>', str(line))
        if res is not None:
            if res.group(1):
                host = res.group(1)
                line = body.readline()
                res = re.search(r'<td>(.*)</td>', str(line))
                port = res.group(1)
                ip.append(host+':'+port)
        line = body.readline()


def start(catch_path, save_path):
    dispose_data(catch_path)
    nowFile = open(save_path, 'r+')
    for i in ip:
        nowFile.seek(0, 2)
        nowFile.write(i+'\n')
    nowFile.close()


start('ipbody.txt', 'proxyIp.txt')
print('完成')
