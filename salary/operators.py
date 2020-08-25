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
import time
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

    
    def __init__(self,config:type(SalaryConfig)):
        assert config is not None
        self.conf = config
        self.logger = SalaryLogging(self.conf).getLogger()


    def loaddatas(self,validatable=True):
        raise NotImplementedError

    def valdator(self,dataitems):
        raise NotImplementedError

    def converter(self):
        raise NotImplementedError

    def writer(self):
        raise NotImplementedError 

    def loaddata(self,tpl_file_path,colnames_index=1,validable=True):
        assert tpl_file_path is not None
        # load 模板数据
        # 加载数据
        # 读取文件
        wb = self.readfile(tpl_file_path)
        # 读取第一个工作部
        if not wb is None:
            sh_0 = wb.sheet_by_index(0)
            # 获取列名
            cols = self.get_column_names(sh_0,colnames_index)
            # 获取数值
            return self.get_data_def(sh_0,cols,colnames_index,validable)
        return list(),list()    

    def get_file_path(self, filefolderpath,filename):
        '''位于主程序目录下的位置
        '''
        return os.path.join(os.getcwd(),filefolderpath,filename)

    def readfile(self,filepath):
        ''' 读取模板文件
        '''
        if not os.path.exists(filepath):
            self.logger.debug(f'{filepath}不存在!')
            return
        return xlrd.open_workbook(filepath)

    def get_column_names(self,sheet,column_name_index=1):
        '''获得列名list
        '''
        cols = sheet.row_slice(column_name_index-1)
        rel = list()
        for c in cols:
            rel.append(c.value)
        return rel
    
    def get_data_def(self,sheet,columnnames,column_name_index=1,vali=True):
        ''' 获取数据信息
        '''
        rows_num = sheet.nrows
        if column_name_index - 1 > rows_num:
            raise ReadTpLError()
        start_nrow = column_name_index
        
        rel = list()
        # 错误信息
        errs = list()
        for sn in range(start_nrow,rows_num):
            cols = sheet.row_slice(sn)
            typs = sheet.row_types(sn)
            # 数据信息
            items = list()
            
            for cn in range(0,len(cols)):
                typ = typs[cn]
                col_name = columnnames[cn]
                items.append(DataItem('code',col_name,cn,typ,cols[cn].value))
            dis = DataItms(sn,items,False)
            rel.append(dis)
            if vali:
                v,err = self.valdator(dis)
                if not v:
                    errs.extend(err)
        return rel,errs

    def get_item_by_colname(self,dataitems,col_name):
        '''获取某列得值
        '''
        for item in dataitems.items:
            if item.col_name.lower() == col_name.lower():
                return item
        return None

class GzOperator(Operator):

    def __init__(self,config:type(SalaryConfig),validatable = True):
        Operator.__init__(self,config)
        self.name = '工资模板处理器'
        self.colnames_index = 1
        # 是否在数据装载时进行数据效验
        self.validable = validatable

    def loaddatas(self): 
        # load 模板数据
        return self.loaddata(self.get_file_path(self.conf.get_tpl_root_folder_name(),self.conf.get_tpl_gz_filename()),self.colnames_index,self.valdator)
    
    
    def valdator(self,dataitems):
        # 实发小于0
        err = list()
        sf = self.get_item_by_colname(dataitems,'实发')
        if sf.val < 0 :
           err.append(f'错误：{dataitems.no}行，实发{sf.val}小于0') 
           return False,err
        return True,None
    
    
    def writer(self,datas,errs):
        '''完成错误信息输出
        '''
        now = int(time.time()) 
        #转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S" 
        timeStruct = time.localtime(now) 
        strTime = time.strftime("%Y-%m-%d-%H-%M-%S", timeStruct) 
        err_file = f'数据核对结果-{strTime}.txt'
        for err in errs:
            with open(err_file,'a') as f:
                f.write(err)
                f.write('\n')

class MergeOperator(Operator):
    ''' 工资、奖金、银行卡信息合并操作
    '''
    def __init__(self,conf:type(SalaryConfig)):
        assert conf is not None
        Operator.__init__(self,conf)
        self.clear_datas()

    def clear_datas(self):
        self.datas = dict()
        self.datas['gz'] = list()
        self.datas['jj'] = list()
        self.datas['yhk'] = list()
    
    def loaddatas(self):
        # 读取工资模板
        # 读取奖金模板
        # 读取银行卡号
        # 组装成
        # gzs,_ = self.readfile(self.get_file_path())
        pass
           

    def read_gz_datas(self):
        pass

        





        

        
