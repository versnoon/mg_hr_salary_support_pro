#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_salary.py
@Time    :   2020/08/18 09:54:19
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''

import pytest
from salary.config import SalaryConfig
from salary import contants



class TestSalaryConfig(object):

    
    def test_config_create_with_default(self):
        conf = SalaryConfig()
        # default settings
        assert conf.config_size() > 0
        assert conf.contains(contants.PRO_NAME_KEY_NAME)
        assert conf.get_pro_name() == 'salary_support_pro'
    

    def test_get_conf_val_with_keyerror(self):
        conf = SalaryConfig()
        with pytest.raises(KeyError):
            conf.get_config_val('errorkey')

    def test_get_conf_val(self):
        conf = SalaryConfig()
        assert conf.get_pro_name() == 'salary_support_pro'
    
    def test_get_logging_name(self):
        conf = SalaryConfig()
        assert conf.get_logging_name() == 'salary_support_logging'
    
    def test_get_logging_level(self):
        conf = SalaryConfig()
        assert conf.get_logging_level() == 'DEBUG'

    def test_get_tpl_gz_filename(self):
        conf = SalaryConfig()
        assert conf.get_tpl_gz_filename() == '工资数据.xls'

    def test_get_tpl_root_folder_name(self):
        conf = SalaryConfig()
        assert conf.get_tpl_root_folder_name() == '宝武EHR数据'
        



    
    