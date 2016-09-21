# -*- encoding=utf-8 -*-
# Python 3.5
# 整理代理ip，去重


class TidyIp:
    def __init__(self, check_all, fail_path, check_path):
        self.fail_path = fail_path
        self.check_path = check_path
        # 是否删除与失效ip重复的ip
        self.checkAll = check_all
        self.failIp = []
        self.trueIp = []

    def start(self):
        if self.checkAll:
            file2 = open(self.fail_path, 'r+')
            for ip in file2.readlines():
                ip = ip.replace('\n', '')
                self.failIp.append(ip)
            file2.close()
        file = open(self.check_path, 'r+')
        ips = file.readlines()
        file.seek(0)
        file.truncate()
        for ip in ips:
            ip = ip.replace('\n', '')
            if ip not in self.trueIp and ip not in self.failIp:
                self.trueIp.append(ip)

        for ip in self.trueIp:
            file.seek(0, 1)
            file.write(ip+'\n')

        file.close()
