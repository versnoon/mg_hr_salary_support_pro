#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   split.py
@Time    :   2020/08/28 11:07:41
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''

import os

from salary.config import SalaryConfig
from salary.operators import Operator


class SalaryTplSplit(Operator):
    ''' 完成模板按照单位切分
    '''
    def __init__(self,config:type(SalaryConfig)):
        Operator.__init__(self,config)
        self.split_col_index = 2 

    def loaddatas(self):
        '''读取文件
        '''
        return self.batchloaddata(self.get_split_file_path_root(),1,False,'split')

    def writer(self,datas):
        ''' 切分写入相应的文件
        '''
        
        # 按照部门切分
        # 默认按照第二部分内容  
        # 
        # 马钢集团>人力资源服务中心
        #     1         2
        self.to_map(datas,self.split_col_index)


    def get_split_file_path_root(self):
        return os.path.join(os.getcwd(),self.conf.tpl_split_file_folder_path(),self.period)

    def to_map(self,datas,split_col_index):
        rel = dict()
        for _ in datas:
           pass   
        return rel

    def get_bm_desc(self,dataitems,split_col_index):
            _,_,depart = self.get_employ_code_name_depart_message_from_items(dataitems)
            if depart is not None and len(depart)>0:
                ds = depart.split('>')
                end_index = split_col_index
                if len(ds) < split_col_index:
                    end_index = len(ds)
                return '-'.join(ds[0:end_index])
         