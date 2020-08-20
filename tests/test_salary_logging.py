#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_salary.py
@Time    :   2020/08/18 09:54:19
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''

from salary.config import SalaryConfig
from salary.logging import SalaryLogging

class TestSalaryLogging():
    ''' logging 模块相关测试
    '''

    def test_create_logger(self):
        config = SalaryConfig()
        logger = SalaryLogging(config).getLogger()
        assert logger is not None
        assert logger.name == 'salary_support_logging'

    def test_logging_filename(self):
       assert SalaryLogging.get_Logging_filename() == '2020-08-20-logs.log'    
