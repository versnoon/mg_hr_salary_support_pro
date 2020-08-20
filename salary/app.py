#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2020/08/17 16:33:03
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''

import os
from salary.config import SalaryConfig


class SalarySupport(object):
    

    def __init__(self,conf: type(SalaryConfig)=None):
        self._config = conf

    
    def run(self) -> 'str':
        return 'salary_run'

if __name__ == "__main__":
    print(SalarySupport().run())

