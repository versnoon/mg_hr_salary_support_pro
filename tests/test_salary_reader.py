#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_salary_reader.py
@Time    :   2020/08/20 16:52:01
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''
import os
import pytest

from salary.operators import Operator
from salary.operators import GzOperator 
from salary.config import SalaryConfig
from salary import contants 

class TestSalaryReader(object):

    def test_create_reader(self):
        op = Operator()
        with pytest.raises(NotImplementedError):
            op.loaddatas()

    def test_get_file_path(self):
        op = Operator()
        getstr = op.get_file_path('文件夹','文件名.文件后缀')
        assert getstr == os.path.join(r'd:\programming\python_projects\mg_hr_salary_support_pro','文件夹','文件名.文件后缀')

    def test_get_file_cols(self):
        op = GzOperator(SalaryConfig())
        wb = op.readfile()
        assert wb is not None
        cols = op.get_column_names(wb.sheet_by_index(0),op.colnames_index)
        assert cols is not None
        assert len(cols) == 102
        assert cols[0].strip() == '员工通行证'

    def test_get_file_items(self):
        op = GzOperator(SalaryConfig())
        wb = op.readfile()
        assert wb is not None
        sh_0 = wb.sheet_by_index(0)
        assert sh_0 is not None
        cols = op.get_column_names(sh_0,op.colnames_index)
        items = op.get_data_def(sh_0,cols,op.colnames_index)
        assert cols is not None
        assert len(items) == 18055
        assert len(items[0].items) == 102
        assert items[0].skip == False


        
