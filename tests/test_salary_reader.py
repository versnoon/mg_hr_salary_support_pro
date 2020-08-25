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
        op = Operator(SalaryConfig())
        with pytest.raises(NotImplementedError):
            op.loaddatas()

    def test_get_file_path(self):
        op = Operator(SalaryConfig())
        getstr = op.get_file_path('文件夹','文件名.文件后缀')
        assert getstr == os.path.join(r'd:\programming\python_projects\mg_hr_salary_support_pro','文件夹','文件名.文件后缀')

    def test_get_file_cols(self):
        op = GzOperator(SalaryConfig())
        wb = op.readfile(op.get_file_path(op.conf.get_tpl_root_folder_name(),op.conf.get_tpl_gz_filename()))
        assert wb is not None
        cols = op.get_column_names(wb.sheet_by_index(0),op.colnames_index)
        assert cols is not None
        assert len(cols) == 102
        assert cols[0].strip() == '员工通行证'

    def test_get_file_items(self):
        op = GzOperator(SalaryConfig())
        wb = op.readfile(op.get_file_path(op.conf.get_tpl_root_folder_name(),op.conf.get_tpl_gz_filename()))
        assert wb is not None
        sh_0 = wb.sheet_by_index(0)
        assert sh_0 is not None
        cols = op.get_column_names(sh_0,op.colnames_index)
        items,_ = op.get_data_def(sh_0,cols,op.colnames_index)
        assert cols is not None
        assert len(items) == 18055
        assert len(items[0].items) == 102
        assert items[0].skip == False
        assert items[0].items[2].val.strip() == r'马鞍山钢铁股份有限公司（总部）\资源分公司\第二回收分厂\回收作业区'
        assert items[0].items[2].col_name.strip() == '机构'
        assert items[0].items[2].typ == 1
        assert items[0].items[11].col_name.strip() == r'累计住房贷款利息支出'
        assert items[0].items[11].val == 8000
        assert items[0].items[11].typ == 2
        assert items[0].items[9].typ == 0

    
    def test_get_item_value(self):
        op = GzOperator(SalaryConfig())
        items,_ = op.loaddatas()
        for item in items:
            col = op.get_item_by_colname(item,'实发')
            assert col is not None
            assert col.typ == 2
            if col.val < 0:
                op.logger.error(f'错误信息:{item.no}行，实发合计小于0。系统计算金额{col.val}')
        err_col = op.get_item_by_colname(items[0],'异常')
        assert err_col is None


        
