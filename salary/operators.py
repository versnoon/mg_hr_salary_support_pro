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
import unicodedata
import xlrd
from salary.config import SalaryConfig
from salary.logging import SalaryLogging
from salary.process import Process
from salary import contants


class ReadTpLError(Exception):
    pass


class ListToMapKeyNotFoundError(Exception):
    pass


class DataItem(object):
    '''
    '''

    def __init__(self, code, col_name, col_index, typ, val):
        self.code = code  # 字段编码
        self.col_name = col_name  # 列名
        self.col_index = col_index  # 显示序号
        self.typ = typ  # 类型
        self.val = val  # 值

    def __str__(self):
        return f'DataItem info code:{self.code},col_name:{self.col_name},col_index:{self.col_index},typ:{self.typ},val:{self.val}'


class DataItms(object):
    '''
    '''

    def __init__(self, no, code, items=list(), skip=False):
        self.no = no
        self.code = code
        self.items = items
        self.skip = skip


class Operator(object):

    def __init__(self, config: type(SalaryConfig)):
        assert config is not None
        self.conf = config
        self.logger = SalaryLogging(self.conf).getLogger()

    def loaddatas(self):
        raise NotImplementedError

    def valdator(self, dataitems):
        raise NotImplementedError

    def converter(self):
        raise NotImplementedError

    def writer(self):
        raise NotImplementedError

    def loaddata(self, tpl_file_path, colnames_index=1, validable=True, code='code'):
        assert tpl_file_path is not None
        # load 模板数据
        # 加载数据
        # 读取文件
        wb = self.readfile(tpl_file_path)
        # 读取第一个工作部
        if not wb is None:
            sh_0 = wb.sheet_by_index(0)
            # 获取列名
            cols = self.get_column_names(sh_0, colnames_index)
            # 获取数值
            return self.get_data_def(sh_0, cols, colnames_index, validable, code)
        return list(), list()

    def __get_file_path(self, filefolderpath, filename):
        '''位于主程序目录下的位置
        '''
        return os.path.join(os.getcwd(), filefolderpath, filename)

    def get_file_path(self, filename):
        return self.__get_file_path(self.conf.get_tpl_root_folder_name(), filename)

    def readfile(self, filepath):
        ''' 读取模板文件
        '''
        if not os.path.exists(filepath):
            self.logger.debug(f'{filepath}不存在!')
            return
        return xlrd.open_workbook(filepath)

    def get_column_names(self, sheet, column_name_index=1):
        '''获得列名list
        '''
        cols = sheet.row_slice(column_name_index-1)
        rel = list()
        for c in cols:
            rel.append(c.value)
        return rel

    def get_data_def(self, sheet, columnnames, column_name_index, vali, code):
        ''' 获取数据信息
        '''
        rows_num = sheet.nrows
        if column_name_index - 1 > rows_num:
            raise ReadTpLError()
        start_nrow = column_name_index

        rel = list()
        # 错误信息
        errs = list()
        for sn in range(start_nrow, rows_num):
            cols = sheet.row_slice(sn)
            typs = sheet.row_types(sn)
            # 数据信息
            items = list()

            for cn in range(0, len(cols)):
                typ = typs[cn]
                col_name = columnnames[cn]
                items.append(DataItem(code, col_name, cn, typ, cols[cn].value))
            dis = DataItms(sn, code, items, False)
            rel.append(dis)
            if vali:
                v, err = self.valdator(dis)
                if not v:
                    errs.extend(err)
        return rel, errs

    def get_item_by_colname(self, dataitems, col_name):
        '''获取某列得值
        '''
        for item in dataitems.items:
            if item.col_name.lower() == col_name.lower():
                return item
        return None

    def get_employ_code_name_depart_message_from_items(self, dataitems):
        '''获取某列得值
        '''
        code = ''
        name = ''
        depart = ''
        for item in dataitems.items:
            if item.col_name.lower() == self.conf.get_tpl_code_column_name():
                code = item.val
            elif item.col_name.lower() == self.conf.get_tpl_name_column_name():
                name = item.val
            elif item.col_name.lower() == self.conf.get_tpl_depart_column_name() or item.col_name.lower() == self.conf.get_tpl_depart_other_column_name():
                depart = item.val.replace('\\', '-')
        return code, name, depart

    def to_map(self, dataitems, keyname):
        rel = dict()
        for di in dataitems:
            key_item = self.get_item_by_colname(di, keyname)
            key = self.get_key_str_from_item(key_item)
            val_list = list()
            if key in rel:
                val_list = rel.get(key)
            val_list.append(di)
            rel[key] = val_list
        return rel

    def get_key_str_from_item(self, key_item):
        if key_item is None:
            raise ListToMapKeyNotFoundError()
        kv = key_item.val
        kvstr = ''
        k_typ = key_item.typ
        # empty 0 blank 6 error 5 boolean 4 date 3
        if k_typ == 0 or k_typ == 6 or k_typ == 3 or k_typ == 5:
            raise ListToMapKeyNotFoundError()
        elif k_typ == 2:
            kvstr = str(kv)
        else:
            kvstr = kv
        return kvstr


class GzOperator(Operator):

    def __init__(self, config: type(SalaryConfig)):
        Operator.__init__(self, config)
        self.name = '工资模板处理器'
        self.colnames_index = 1
        # 是否在数据装载时进行数据效验
        self.validable = True

    def unvalid(self):
        self.validable = False

    def loaddatas(self):
        # load 模板数据
        return self.loaddata(self.get_file_path(self.conf.get_tpl_gz_filename()), self.colnames_index, self.valdator)

    def valdator(self, dataitems):
        # 实发小于0
        err = list()
        sf = self.get_item_by_colname(dataitems, '实发')
        if sf.val < 0:
            err.append(f'错误：{dataitems.no}行，实发{sf.val}小于0')
            return False, err
        return True, None

    def writer(self, datas, errs):
        '''完成错误信息输出
        '''
        now = int(time.time())
        # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
        timeStruct = time.localtime(now)
        strTime = time.strftime("%Y-%m-%d-%H-%M-%S", timeStruct)
        err_file = f'数据核对结果-{strTime}.txt'
        for err in errs:
            with open(err_file, 'a') as f:
                f.write(err)
                f.write('\n')


class MergeOperator(Operator):
    ''' 工资、奖金、银行卡信息合并操作
    '''

    def __init__(self, conf: type(SalaryConfig)):
        assert conf is not None
        Operator.__init__(self, conf)
        self.clear_datas()
        self.name = '工资奖金模板处理器'

    def clear_datas(self):
        self.datas = dict()
        self.datas['gz'] = list()
        self.datas['jj'] = list()
        self.datas['yhk'] = list()

    def loaddatas(self):
        # 读取工资模板
        gz_tpl_path = self.get_file_path(self.conf.get_tpl_gz_filename())
        gzs, _ = self.loaddata(gz_tpl_path, 1, False, 'gz')
        if len(gzs) > 0:
            self.datas['gz'] = gzs
        # 读取奖金模板
        jj_tpl_path = self.get_file_path(self.conf.get_tpl_jj_filename())
        jjs, _ = self.loaddata(jj_tpl_path, 1, False, 'jj')
        if len(jjs) > 0:
            self.datas['jj'] = jjs
        # 读取银行卡号
        yhk_tpl_path = self.get_file_path(self.conf.get_tpl_yhk_filename())
        yhks, _ = self.loaddata(yhk_tpl_path, 1, False, 'yhk')
        if len(yhks) > 0:
            self.datas['yhk'] = yhks
        return self.merge_valdator()

    # 验证
    def merge_valdator(self):
        key_col_name = self.conf.get_tpl_map_key_column_name()
        gz_map = self.to_map(self.datas['gz'], key_col_name)
        jj_map = self.to_map(self.datas['jj'], key_col_name)
        yhk_map = self.to_map(self.datas['yhk'], key_col_name)

        errs = list()
        errs.extend(self.valdate(gz_map,yhk_map,'gz'))
        errs.extend(self.valdate(jj_map,yhk_map,'jj'))
        # 验证工资数据
        # 没有工资发放记录
        # 存在多条工资发放记录
        # 工资奖金实发不为0
        # 工资实发大于0 工资账号不为空
        # 存在多条奖金发放记录
        # 奖金实发大于0 奖金账号不为空

        return list(), errs

    def writer(self, datas, errs):
        '''完成错误信息输出
        '''
        now = int(time.time())
        # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
        timeStruct = time.localtime(now)
        strTime = time.strftime("%Y-%m-%d-%H-%M-%S", timeStruct)
        err_file = f'数据核对结果-{strTime}.txt'
        if len(errs) == 0:
            with open(err_file, 'a') as f:
                f.write('数据验证通过')
        else:
            for err in sorted(errs):
                with open(err_file, 'a') as f:
                    f.write(err)
                    f.write('\n')

    def get_err_message(self, dataitemss, msg):
        dataitems = dataitemss[0]
        typ = dataitems.code
        msg_prefix = self.get_err_message_prefix(typ)
        code, name, depart = self.get_employ_code_name_depart_message_from_items(
            dataitems)
        nos = self.get_err_message_nos(dataitemss)
        return f'{code}-{name}-{depart}  {msg_prefix}: {msg}--->{nos}'

    def get_err_message_prefix(self, typ):
        msg_prefix = '信息'
        if typ == 'gz':
            msg_prefix = f'工资{msg_prefix}'
        elif typ == 'jj':
            msg_prefix = f'奖金{msg_prefix}'
        elif typ == 'yhk':
            msg_prefix = f'银行卡{msg_prefix}'
        return msg_prefix

    def get_err_message_nos(self, dataitemss):
        nos = list()
        nos.append('相关行号: ')
        for dataitems in dataitemss:
            nos.append(f'{str(dataitems.no)}行,')
        return ' '.join(nos)

    def get_yhk_typ_str(self,yhk_typ):
        if yhk_typ == 'gz':
            return '工资'
        elif yhk_typ == 'jj':
            return '奖金'
        else:
            return '未知'
    def get_yhk_no(self, yhks,yhk_typ):
        typ = f'{self.get_yhk_typ_str(yhk_typ)}卡'
        for yhk in yhks:
            yhk_item = self.get_item_by_colname(yhk, '卡用途')
            if yhk_item is not None:
                 if yhk_item.val.find(typ) != -1:
                    yhk_item_no = self.get_item_by_colname(yhk, '卡号')
                    if yhk_item_no is not None and len(yhk_item_no.val) > 0:
                        return yhk_item_no.val
                    else:
                        return ''
        return ''

    def valdate(self,data_map,yhk_map,typ):
        typ_str = f'{self.get_yhk_typ_str(typ)}'
        errs = list()
        for k, v in data_map.items():
            if len(v) == 0:
                errs.append(self.get_err_message(v, f'没有{typ_str}发放记录'))
            elif len(v) > 1:
                errs.append(self.get_err_message(v, f'存在多条{typ_str}发放记录'))
            else:
                # 验证实发小于0
                sf = self.get_item_by_colname(v[0], '实发')
                if sf.val < 0:
                    errs.append(self.get_err_message(v, f'实发{sf.val}小于0'))
                # 验证卡号
                elif sf.val != 0:
                    if len(yhk_map) > 0:
                        if k not in yhk_map:
                            errs.append(self.get_err_message(v, f'缺少{typ_str}卡信息'))
                        else:
                            yhks = yhk_map.get(k)
                            yhk_no = self.get_yhk_no(yhks,typ).strip()
                            if len(yhk_no) == 0:
                                errs.append(self.get_err_message(v, f'缺少{typ_str}卡信息'))
                # 验证缺少岗位工资
                gwgz = self.get_item_by_colname(v[0], '岗位工资')
                xcms = self.get_item_by_colname(v[0], '薪酬模式')
                if gwgz is not None and gwgz.val == 0 and xcms is not None and xcms.val == '岗位绩效工资制' :
                    errs.append(self.get_err_message(v, f'缺少{typ_str}岗位工资信息'))
                # 验证保留劳动关系 停薪留职实发不为0 (缺少信息无法实现)
        return errs
