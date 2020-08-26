#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   runner.py
@Time    :   2020/08/17 16:32:23
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''

import os

from salary.app import SalarySupport


if __name__ == "__main__":
    #  eg app.run(相关配置)
    msg = SalarySupport().run()
    print(msg)
    input("回车退出程序!")