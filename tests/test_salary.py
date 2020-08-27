#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_salary.py
@Time    :   2020/08/18 09:54:19
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''
from pytest_mock import mock

from salary.config import SalaryConfig
from salary.app import SalarySupport



class TestSalary(object):
    

    @mock.patch('builtins.input', side_effect=['202009'])
    def test_salary_support_run(self,capsys):
       with capsys.disabled():
            s = SalarySupport()
            a = s.run()
            expected = '效验通过'
            assert a == expected
            

    def test_get_period_now(self):
        su = SalarySupport()
        s = su.get_period_now()
        assert s == '202008' 

    @mock.patch('builtins.input', side_effect=['202009','20209',''])
    def test_input_period(self,input):
        su = SalarySupport()
        s = su.input_period()
        assert s == '202009'
        s = su.input_period()
        assert s == su.get_period_now()
        assert su.input_period() == su.get_period_now()
