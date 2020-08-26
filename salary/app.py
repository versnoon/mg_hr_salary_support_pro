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
from salary.process import Process
from salary.operators import MergeOperator


class SalarySupport(object):
    

    def __init__(self,conf: type(SalaryConfig)=None):
        if conf is None:
            conf = SalaryConfig()
        self._config = conf

    
    def run(self) -> 'str':
        proc = Process(MergeOperator(self._config))
        val = proc.process_validat()
        msg = '效验通过'
        if not val:
            msg = '效验失败,请查看数据核对结果文件'
        return msg


