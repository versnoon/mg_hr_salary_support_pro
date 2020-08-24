#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   logging.py
@Time    :   2020/08/20 14:21:53
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''
import logging
import time

from salary import contants
from salary.config import SalaryConfig


class SalaryLogging(object):
    '''日志模块抽象类
    '''

    def __init__(self,config:type(SalaryConfig)):
        assert config is not None
        self.logger = self.__init_logging(config)
        

    def __init_logging(self,config:type(SalaryConfig)):
        logger = logging.getLogger(config.get_logging_name())
        logger.setLevel(logging.DEBUG)
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.get_Logging_filename(), 'a', encoding='utf-8') 
        fh.setLevel(config.get_logging_level())
        fh.setFormatter(logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s'))
        logger.addHandler(fh)
        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s'))
        logger.addHandler(ch)
        
        return logger

    def get_Logging_filename(self):
        return '%s-logs.log' % time.strftime('%Y-%m-%d')

    def getLogger(self):
        return self.logger



    