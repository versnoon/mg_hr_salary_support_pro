#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test.salary_process.py
@Time    :   2020/08/24 13:21:52
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''



from salary.process import  Process 
from salary.operators import GzOperator
from salary.config import SalaryConfig

class TestSalaryProcess(object):

    def test_gz_opreator_process(self):
        proc = Process(GzOperator(SalaryConfig()))
        proc.process_validat()
        assert proc.name == '工资模板处理器' 