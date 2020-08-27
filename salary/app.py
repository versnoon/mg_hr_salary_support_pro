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
import datetime
import re

from salary.config import SalaryConfig
from salary.process import Process
from salary.operators import MergeOperator


class SalarySupport(object):

    def __init__(self, conf: type(SalaryConfig) = None):
        if conf is None:
            conf = SalaryConfig()
        self._config = conf

    def run(self) -> 'str':
        # 选择时间段
        period = self.input_period()
        proc = Process(MergeOperator(self._config),period)
        val = proc.process_validat()
        msg = '效验通过'
        if not val:
            msg = '效验失败,请查看数据核对结果文件'
        return msg

    def get_period_now(self):
        now = datetime.datetime.now()
        return now.strftime('%Y%m')

    def input_period(self):
        def_period = self.get_period_now()
        period_input = input(f'请输入年份：默认为{def_period}')
        if period_input == '':
            period_input = def_period
        r = re.compile(r'\d{6}')
        if not r.match(period_input):
            period_input = def_period
        return period_input

