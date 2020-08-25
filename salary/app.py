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

os.sys.path.append(os.path.realpath(os.getcwd()))
from salary.config import SalaryConfig
from salary.process import Process
from salary.operators import GzOperator


class SalarySupport(object):
    

    def __init__(self,conf: type(SalaryConfig)=None):
        if conf is None:
            conf = SalaryConfig()
        self._config = conf

    
    def run(self) -> 'str':
        proc = Process(GzOperator(self._config))
        proc.process_validat()
        return 'salary_run'


