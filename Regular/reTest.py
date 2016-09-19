# encoding=utf-8

import re

s = '24418# 2016-08-28 13:31:24:你已成功提现560元。你提交的提\
        现金额将在两个工作日内到账，请关注你的支付宝资金账户余额变动情况。'

res = re.search(r'你已成功提现(.*)元', s)
if res.group():
    print(res.group(1))
else:
    print('nothing')
