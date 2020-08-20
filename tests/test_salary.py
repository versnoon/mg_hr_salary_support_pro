#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_salary.py
@Time    :   2020/08/18 09:54:19
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''

from salary.config import settings 
from salary.config import SalaryConfig
from salary.app import SalarySupport



class TestSalary(object):
    

    def test_salary_support_run(self):
        a = SalarySupport().run()
        expected = 'salary_run'
        assert a == expected
