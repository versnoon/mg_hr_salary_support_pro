#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_salary_operator_split.py
@Time    :   2020/08/28 13:20:25
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''

import os

from salary.config import SalaryConfig
from salary.split_operator import SalaryTplSplit
from salary.operators import DataItms
from salary.operators import DataItem

class TestSalaryTplSplit():


    def test_get_split_file_path_root(self):
        config = SalaryConfig()
        split = SalaryTplSplit(config)
        split.set_period('202008')
        path = split.get_split_file_path_root()
        assert path is not None
        assert path == os.path.join(os.getcwd(),config.tpl_split_file_folder_path(),'202008')

    def test_get_bm_desc(self):
        config = SalaryConfig()
        split = SalaryTplSplit(config)
        split.set_period('202008')
        dataitems = DataItms(0,'gz',[DataItem('gz','员工通行证',0,1,'M73247'),DataItem('gz','员工姓名',1,1,'张志容'),DataItem('gz','机构',2,1,r'马鞍山钢铁股份有限公司（总部）\资源分公司\第二回收分厂\回收作业区')])
        bm = split.get_bm_desc(dataitems,2)
        assert bm == '马鞍山钢铁股份有限公司（总部）-资源分公司'
        bm = split.get_bm_desc(dataitems,3)
        assert bm == '马鞍山钢铁股份有限公司（总部）-资源分公司-第二回收分厂'
        bm = split.get_bm_desc(dataitems,100)
        assert bm == '马鞍山钢铁股份有限公司（总部）-资源分公司-第二回收分厂-回收作业区'