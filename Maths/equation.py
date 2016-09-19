# encoding=utf-8
#
# Python Version 3.5
# 利用数学中的复数 求解 一元一次方程(从网上看来的)


def solve(qx, var):
    qx = qx.replace('=', '-(') + ')'
    c = eval(qx , {var: 1j})
    return -c.real/c.imag

res = solve('2*x + 4 = 8','x')
print(res)




