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
        assert len(conf.get_config_dict()) > 0
        assert contants.PRO_NAME_KEY_NAME in conf.get_config_dict()
        assert conf.get_config_dict().get(contants.PRO_NAME_KEY_NAME) == 'salary_support_pro'
    

    def test_get_conf_val_with_keyerror(self):
        conf = SalaryConfig()
        with pytest.raises(KeyError):
            conf.get_config_val('errorkey')

    def test_get_conf_val(self):
        conf = SalaryConfig()
        assert conf.get_config_dict().get(contants.PRO_NAME_KEY_NAME) == 'salary_support_pro'



    
    