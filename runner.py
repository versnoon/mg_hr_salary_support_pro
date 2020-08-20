#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   runner.py
@Time    :   2020/08/17 16:32:23
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''

from salary.logging import SalaryLogging
from salary.config import SalaryConfig

if __name__ == "__main__":
    #  eg app.run(相关配置)
    logger = SalaryLogging(SalaryConfig()).getLogger()
    logger.error('sys err')
    logger.info('sys info')
    logger.debug('sys debug')