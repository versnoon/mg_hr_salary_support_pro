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
    logger = None

    def __init__(self,salary_conf:type(SalaryConfig)):
        assert salary_conf is not None
        if SalaryLogging.logger == None:
            SalaryLogging.logger = self.__init_logging(salary_conf)

    def __init_logging(self,config:type(SalaryConfig)):
        logger = logging.getLogger(config.get_logging_name())
        logger.setLevel(config.get_logging_level())
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

    @staticmethod
    def get_Logging_filename():
        return '%s-logs.log' % time.strftime('%Y-%m-%d')

    @staticmethod
    def getLogger():
        return SalaryLogging.logger

    def error(self, msg):
        log = SalaryLogging.getLogger()
        log.error(msg)

    def warn(self, msg):
        log = SalaryLogging.getLogger()
        log.warning(msg)

    def info(self, msg):
        log = SalaryLogging.getLogger()
        log.info(msg)

    def debug(self, msg):
        log = SalaryLogging.getLogger()
        log.debug(msg)

    def exception(self, msg):
        """
        打印堆栈信息
        :param msg:
        :param name:
        :return:
        """
        log = SalaryLogging.getLogger()
        log.exception(msg)


    