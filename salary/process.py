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


    def __init__(self,operator):
        self.operator = operator
        self.name = self.operator.name

    def process(self):
        datas = self.operator.loaddatas()
        model_datas = self.operator.converter(datas)
        self.operator.writer(model_datas)

    def process_validat(self):
        datas,errs = self.operator.loaddatas()
        self.operator.writer(datas,errs)
    