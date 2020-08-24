#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   readers.py
@Time    :   2020/08/20 16:39:50
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''

import os
import xlrd
from salary.config import SalaryConfig
from salary.logging import SalaryLogging
from salary.process import Process
from salary import contants

class ReadTpLError(Exception):
    pass

class DataItem(object):
    '''
    '''
    def __init__(self, code,col_name,col_index,typ,val):
        self.code = code # 字段编码
        self.col_name = col_name  # 列名
        self.col_index = col_index # 显示序号
        self.typ = typ # 类型
        self.val = val # 值


    def __str__(self):
        return f'DataItem info code:{self.code},col_name:{self.col_name},col_index:{self.col_index},typ:{self.typ},val:{self.val}'  

class DataItms(object):
    '''
    '''
    def __init__(self,no,items=list(),skip=False):
        self.no = no
        self.items = items
        self.skip = skip 

class Operator(object):

    
    def __init__(self,config:type(SalaryConfig)=None):
        self.conf = config
        self.logger = SalaryLogging(SalaryConfig()).getLogger()


    def loaddatas(self):
        raise NotImplementedError

    def converter(self):
        raise NotImplementedError

    def writer(self):
        raise NotImplementedError     

    def get_file_path(self, filefolderpath,filename):
        '''位于主程序目录下的位置
        '''
        return os.path.join(os.getcwd(),filefolderpath,filename)

    def readfile(self):
        filepath = self.get_file_path(self.conf.get_tpl_root_folder_name(),self.conf.get_tpl_gz_filename())
        if not os.path.exists(filepath):
            self.logger.debug(f'{filepath}不存在!')
            return
        return xlrd.open_workbook(filepath)

class GzOperator(Operator):

    def __init__(self,config:type(SalaryConfig)):
        Operator.__init__(self,config)
        self.name = '工资模板处理器'
        self.colnames_index = 1

    def loaddatas(self): 
        # load 模板数据
        # 加载数据
        # 读取文件
        wb = self.readfile()
        # 读取第一个工作部
        if not wb is None:
            sh_0 = wb.sheet_by_index(0)
            # 获取列名
            cols = self.get_column_names(sh_0,self.colnames_index)
            # 获取数值
            items = self.get_data_def(sh_0,cols,self.colnames_index)
            return items
        return list()
     

    def get_column_names(self,sheet,column_name_index):
        cols = sheet.row_slice(column_name_index-1)
        rel = list()
        for c in cols:
            rel.append(c.value)
        return rel
    def get_data_def(self,sheet,columnnames,column_name_index):
        rows_num = sheet.nrows
        if column_name_index - 1 > rows_num:
            raise ReadTpLError()
        start_nrow = column_name_index
        
        rel = list()
        for sn in range(start_nrow,rows_num):
            cols = sheet.row_slice(sn)
            typs = sheet.row_types(sn)
            items = list()
            for cn in range(0,len(cols)):
                typ = typs[cn]
                col_name = columnnames[cn]
                items.append(DataItem('code',col_name,cn,typ,cols[cn]))
            rel.append(DataItms(sn,items,False))
        return rel
    
    def converter(self,datas):
        '''转换为工资数据model
        '''
        rel = list()
        for d in datas:
            rel.append(self.to_gz(d))
        return rel

    def writer(self,datas):
        '''
        '''
        return datas

    def to_gz(self,datas):
        '''转换
        '''
        pass
            





        

        
