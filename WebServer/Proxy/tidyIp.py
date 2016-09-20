# -*- encoding=utf-8 -*-
# Python 3.5
# 整理代理ip，去重

file2 = open('failip.txt', 'r+')
failIp = []
for ip in file2.readlines():
    ip = ip.replace('\n', '')
    failIp.append(ip)
file2.close()

file = open('proxyIp.txt', 'r+')
ips = file.readlines()
file.seek(0)
file.truncate()

trueIp = []

for ip in ips:
    ip = ip.replace('\n', '')
    if ip not in trueIp and ip not in failIp:
        trueIp.append(ip)

for ip in trueIp:
    file.seek(0, 1)
    file.write(ip+'\n')

file.close()
