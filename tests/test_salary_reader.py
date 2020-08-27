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
from salary.operators import MergeOperator
from salary.operators import DataItms
from salary.operators import DataItem
from salary.operators import ListToMapKeyNotFoundError
from salary.config import SalaryConfig
from salary import contants 

class TestSalaryReader(object):

    def test_create_reader(self):
        op = Operator(SalaryConfig())
        with pytest.raises(NotImplementedError):
            op.loaddatas()

    def test_get_file_path(self):
        op = Operator(SalaryConfig())
        op.set_period('202008')  
        getstr = op.get_file_path('文件名.文件后缀')
        assert getstr == os.path.join(r'd:\programming\python_projects\mg_hr_salary_support_pro',op.conf.get_tpl_root_folder_name(),op.period,'文件名.文件后缀')

    

    def test_get_file_cols(self):
        op = GzOperator(SalaryConfig())
        op.set_period('202008')
        wb = op.readfile(op.get_file_path(op.conf.get_tpl_gz_filename()))
        assert wb is not None
        cols = op.get_column_names(wb.sheet_by_index(0),op.colnames_index)
        assert cols is not None
        assert len(cols) == 102
        assert cols[0].strip() == '员工通行证'

    def test_gz_operator_valid(self):
        op = GzOperator(SalaryConfig())
        op.set_period('202008')
        assert op.validable == True
        op.unvalid()
        assert op.validable ==  False

    def test_get_file_items(self):
        op = GzOperator(SalaryConfig())
        op.set_period('202008')
        wb = op.readfile(op.get_file_path(op.conf.get_tpl_gz_filename()))
        assert wb is not None
        sh_0 = wb.sheet_by_index(0)
        assert sh_0 is not None
        cols = op.get_column_names(sh_0,op.colnames_index)
        items,_ = op.get_data_def(sh_0,cols,op.colnames_index,False,'gz')
        assert cols is not None
        assert len(items[0].items) == 102
        assert items[0].skip == False
        assert items[0].items[2].col_name.strip() == '机构'
        assert items[0].items[2].typ == 1

    
    def test_get_item_value(self):
        op = GzOperator(SalaryConfig())
        op.set_period('202008')
        items,_ = op.loaddatas()
        for item in items:
            col = op.get_item_by_colname(item,'实发')
            assert col is not None
            assert col.typ == 2
            if col.val < 0:
                op.logger.error(f'错误信息:{item.no}行，实发合计小于0。系统计算金额{col.val}')
        err_col = op.get_item_by_colname(items[0],'异常')
        assert err_col is None

    def test_get_key_str_from_item(self):
        op = GzOperator(SalaryConfig())
        op.set_period('202008')
        items = DataItms(0,'gz',[DataItem('code','员工通行证',0,1,'M73247'),DataItem('code','党费',9,0,''),DataItem('code','累计住房租金支出',10,2,3000)])
        keystr = op.get_key_str_from_item(items.items[0])
        assert keystr == 'M73247'
        with pytest.raises(ListToMapKeyNotFoundError):
            op.get_key_str_from_item(items.items[1])
        keystr = op.get_key_str_from_item(items.items[2])
        assert keystr == str(3000)

    def test_to_map(self):
        op = MergeOperator(SalaryConfig())
        op.set_period('202008')
        items = [DataItms(0,'gz',[DataItem('code','员工通行证',0,1,'M73247'),DataItem('code','党费',9,0,''),DataItem('code','累计住房租金支出',10,2,3000)]),\
                 DataItms(1,'gz',[DataItem('code','员工通行证',0,1,'M73248'),DataItem('code','党费',9,0,''),DataItem('code','累计住房租金支出',10,2,5000)]),\
                 DataItms(2,'gz',[DataItem('code','员工通行证',0,1,'M73249'),DataItem('code','党费',9,0,''),DataItem('code','累计住房租金支出',10,2,8000)]),\
                 DataItms(2,'sap',[DataItem('sap','员工通行证',0,1,'200658'),DataItem('sap','党费',9,0,''),DataItem('sap','累计住房租金支出',10,2,8000)])]

        mps = op.to_map(items,'员工通行证',op.conv_key)
        assert len(mps) == 4
        t = mps.get('M73247') 
        assert t is not None
        assert len(t) == 1
        assert t[0].no == 0
        assert t[0].items[0].col_name == '员工通行证' 
        assert t[0].items[0].val == 'M73247' 
        t = mps.get('MA7333')
        assert t is not None
        assert t[0].items[0].val == '200658' 

    def test_get_employ_code_name_depart_message_from_items(self):
        op = MergeOperator(SalaryConfig())
        op.set_period('202008')
        dataitems = [DataItms(0,'gz',[DataItem('gz','员工通行证',0,1,'M73247'),DataItem('gz','员工姓名',1,1,'张志容'),DataItem('gz','机构',2,1,r'马鞍山钢铁股份有限公司（总部）\资源分公司\第二回收分厂\回收作业区')])]
        code,name,depart = op.get_employ_code_name_depart_message_from_items(dataitems[0])
        assert code == 'M73247'
        assert name == '张志容'
        assert depart == r'马鞍山钢铁股份有限公司（总部）-资源分公司-第二回收分厂-回收作业区'
        errmsg = op.get_err_message(dataitems,'测试信息')
        assert errmsg == f'{code}-{name}-{depart}  工资信息: 测试信息--->相关行号:  0行,'

    def test_get_err_message_prefix(self):
        op = MergeOperator(SalaryConfig())
        op.set_period('202008')
        typ_str = op.get_err_message_prefix('gz')
        assert typ_str == '工资信息'
        typ_str = op.get_err_message_prefix('jj')
        assert typ_str == '奖金信息'
        typ_str = op.get_err_message_prefix('yhk')
        assert typ_str == '银行卡信息'

    def test_merge_opreator_create(self):
        op = MergeOperator(SalaryConfig())
        op.set_period('202008')
        assert op is not None

    def test_get_yhk_no(self):
        op = MergeOperator(SalaryConfig())
        op.set_period('202008')
        dataitemss = [DataItms(0,'yhk',[DataItem('yhk','卡号',4,1,'6215591306000614234'),DataItem('yhk','卡用途',6,1,'报支卡  奖金卡  工资卡')])]
        yhk_no_str = op.get_yhk_no(dataitemss,'gz')
        assert len(yhk_no_str)>0
        assert yhk_no_str == '6215591306000614234'
        
        yhk_no_str = op.get_yhk_no(dataitemss,'jj')
        assert len(yhk_no_str)>0
        assert yhk_no_str == '6215591306000614234'
        
        dataitemss = [DataItms(0,'yhk',[DataItem('yhk','卡号',4,1,'6215591306000614234'),DataItem('yhk','卡用途',6,1,'报支卡  奖金卡')])]

        yhk_no_str = op.get_yhk_no(dataitemss,'gz')
        assert len(yhk_no_str) == 0
        assert yhk_no_str == ''
        yhk_no_str = op.get_yhk_no(dataitemss,'jj')
        assert len(yhk_no_str)>0
        assert yhk_no_str == '6215591306000614234'

        dataitemss = [DataItms(0,'yhk',[DataItem('yhk','卡号',4,1,'6215591306000614234'),DataItem('yhk','卡用途',6,1,'报支卡')])]
        yhk_no_str = op.get_yhk_no(dataitemss,'gz')
        assert len(yhk_no_str) == 0
        assert yhk_no_str == ''
        yhk_no_str = op.get_yhk_no(dataitemss,'jj')
        assert len(yhk_no_str) == 0
        assert yhk_no_str == ''

    
    
    


        
