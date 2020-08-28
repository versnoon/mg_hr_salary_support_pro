#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   process.py
@Time    :   2020/08/24 09:59:20
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''


class Process(object):


    def __init__(self,operator,period):
        self.operator = operator
        self.period = period
        self.name = self.operator.name
        # 设置处理期间
        self.operator.set_period(self.period)

    def process(self):
        datas = self.operator.loaddatas()
        model_datas = self.operator.converter(datas)
        self.operator.writer(model_datas)

    def process_validat(self):
        datas,errs = self.operator.loaddatas()
        if len(errs) > 0:
            self.operator.writer(datas,errs)
            return False
        return True

    def process_split(self):
        datas,_ = self.operator.loaders()
        if len(datas) > 0:
            self.operator.writer(datas)
    