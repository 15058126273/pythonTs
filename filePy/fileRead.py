#  -*- encoding=utf-8 -*-
# python 3.5

import re

pay = 0.00
withdraw = 0
accounts = ''
account_num = 0

file = open('files/all_msg.txt', 'rb')
line = file.readline()
while line:
    line = line.decode()
    if '您已成功充值：' in line:
        num = line.split('您已成功充值：')[1]
        pay += float(num)
    elif '你已成功提现' in line:
        num = re.search(r'你已成功提现(.*)元', line).group(1)
        withdraw += float(num)
    elif '绑定成功' in line:
        account = re.search(r'您的帐号（(.*)）绑定成功', line).group(1)
        accounts += account+'\n'
        account_num += 1
    else:
        pass
    line = file.readline()
print('总充值金额为：', pay)
print('总提现金额为：', withdraw)
accountFile = open('files/accounts.txt', 'w')
accountFile.write('总绑定帐号数：'+str(account_num)+'\n'+accounts)
file.close()
accountFile.close()

