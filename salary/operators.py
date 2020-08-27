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
    
    def set_period(self,period):
        self.period = period

    def loaddatas(self):
        raise NotImplementedError

    def valdator(self, dataitems):
        raise NotImplementedError

    def converter(self):
        raise NotImplementedError

    def writer(self):
        raise NotImplementedError

    # 读取模板目录下所有文件
    def batchloaddata(self,tpl_root_path,colnames_index=1, validable=True, code='gz'):
        datas ,errs = list(),list()
        paths = self.get_tpl_file_paths(tpl_root_path,code)
        for file_path in paths:
            ds,es = self.loaddata(file_path,colnames_index, validable, code)
            datas.extend(ds)
            errs.extend(es)
        return datas,errs
    
    def get_tpl_file_paths(self,tpl_root_path,typ):
        paths = list()
        root = os.path.join(tpl_root_path,self.period,self.get_tpl_folder_path(typ))
        for base_path,_,files in os.walk(root):
            for file_name in files:
                file_path = os.path.join(base_path,file_name)
                if self.is_tpl(file_path,typ):
                    paths.append(file_path)
        return paths
    
    
    def get_tpl_folder_path(self,typ):
        folder_name = ''
        if typ == 'gz':
            folder_name = self.conf.get_tpl_gz_file_folder_name()
        elif typ == 'jj':
            folder_name = self.conf.get_tpl_jj_file_folder_name()
        elif typ == 'yhk':
            folder_name = self.conf.get_tpl_yhk_file_folder_name()
        elif typ == 'sap':
            folder_name = self.conf.get_tpl_sap_file_folder_name()
        return self.get_file_path(folder_name)
    
    def is_tpl(self,file_path,typ):
        ''' 通过文件后缀判断是否为模板
            如果后缀与系统统计相同返回True 
        '''
        file_exts = file_path.rsplit('.',maxsplit=1)
        if len(file_exts) != 2:
            return False
        file_ext = file_exts[1]
        ext = ''
        if typ == 'gz':
            ext = self.conf.get_tpl_gz_file_ext()
        elif typ == 'jj':
            ext = self.conf.get_tpl_jj_file_ext()
        elif typ == 'yhk':
            ext = self.conf.get_tpl_yhk_file_ext()
        elif typ == 'sap':
            ext = self.conf.get_tpl_sap_file_ext()
        return file_ext.lower() == ext.lower()


    def loaddata(self, tpl_file_path, colnames_index=1, validable=True, code='code'):
        assert self.period is not None
        assert self.period != ''
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

    def __get_file_path(self, filefolderpath,period, filename):
        '''位于主程序目录下的位置
        '''
        return os.path.join(os.getcwd(), filefolderpath, period,filename)

    def get_file_path(self, filename):
        return self.__get_file_path(self.conf.get_tpl_root_folder_name(),self.period,filename)

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
            dis = DataItms(sn + 1, code, items, False)
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
    
    def get_employ_sap_code_name_depart_message_from_items(self, dataitems):
        '''获取某列得值
        '''
        code = ''
        name = ''
        depart = ''
        for item in dataitems.items:
            if item.col_name.lower() == '员工编号':
                code = item.val
            elif item.col_name.lower() == '员工姓名':
                name = item.val
            elif item.col_name.lower() == '工资范围':
                depart = item.val
        return code, name, depart

    def to_map(self, dataitems, keyname,conv_key=None):
        rel = dict()
        for di in dataitems:
            key_item = self.get_item_by_colname(di, keyname)
            key = self.get_key_str_from_item(key_item)
            val_list = list()
            if key in rel:
                val_list = rel.get(key)
            val_list.append(di)
            if conv_key is None:
                rel[key] = val_list
            else:
                rel[conv_key(key)] = val_list
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

    def get_err_message(self, dataitemss, msg):
        dataitems = dataitemss[0]
        typ = dataitems.code
        msg_prefix = self.get_err_message_prefix(typ)
        code, name, depart = self.get_employ_code_name_depart_message_from_items(
            dataitems)
        nos = self.get_err_message_nos(dataitemss)
        return f'{code}-{name}-{depart}  {msg_prefix}: {msg}--->{nos}'
    
    def get_err_message_sap(self,sap_itemss,msg):
        dataitems = sap_itemss[0]
        typ = dataitems.code
        msg_prefix = self.get_err_message_prefix(typ)
        code, name, depart = self.get_employ_sap_code_name_depart_message_from_items(
            dataitems)
        nos = self.get_err_message_nos(sap_itemss)
        return f'{self.conv_key(code)}-{name}-{depart}  {msg_prefix}: {msg}--->{nos}'

    def get_err_message_prefix(self, typ):
        msg_prefix = '信息'
        if typ == 'gz':
            msg_prefix = f'工资{msg_prefix}'
        elif typ == 'jj':
            msg_prefix = f'奖金{msg_prefix}'
        elif typ == 'yhk':
            msg_prefix = f'银行卡{msg_prefix}'
        elif typ == 'sap':
            msg_prefix = f'SAP{msg_prefix}'
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

    def conv_key(self,key):
        return self.conf.get_bw_code_from_sap_code(key)

    def item_association(self):
        gz_assocs = dict()
        jj_assocs = dict()
        gz_assocs['岗位工资'] = '岗位工资'
        gz_assocs['保留工资'] = '保留工资'
        gz_assocs['年功工资'] = '工龄工资'
        gz_assocs['辅助工资'] = '其他保留工资'
        gz_assocs['夜班津贴'] = '中夜班津贴'
        gz_assocs['技师津贴'] = '技能津贴'
        gz_assocs['科技津贴'] = '科技优秀津贴'
        gz_assocs['能手津贴'] = '操作能手津贴'
        gz_assocs['外语津贴'] = '学历津贴'
        gz_assocs['教、护龄津贴'] = '驻外津贴'
        gz_assocs['通讯费'] = '通讯补贴'
        gz_assocs['保健费'] = '出勤津贴'
        gz_assocs['独补'] = '独生子女费'
        gz_assocs['防暑降温'] = '高温津贴'
        gz_assocs['回民'] = '民族津贴'
        gz_assocs['技术攻关津贴'] = '技术津贴'
        gz_assocs['科研项目津贴'] = '特殊贡献津贴'
        gz_assocs['职务补贴'] = '公务车贴'
        gz_assocs['非工资性津贴补发'] = '各项补贴'
        gz_assocs['物业补贴'] = '水电气暖物业补贴'
        gz_assocs['预支工资'] = '月固定薪资'
        gz_assocs['法定节日加班工资'] = '法定假日加班工资'
        gz_assocs['公休日加班工资'] = '休息日加班工资'
        gz_assocs['平时加班工资'] = '平常加班工资'
        ## 补充年薪制人员
        
        jj_assocs['基本奖金'] = '基本奖金'
        jj_assocs['单项奖1'] = '单项奖1'
        jj_assocs['单项奖2'] = '单项奖2'
        jj_assocs['单项奖3'] = '单项奖3'
        jj_assocs['计税奖金'] = '计税奖金'
        jj_assocs['年底兑现奖'] = '年底兑现奖'
        jj_assocs['工程津贴'] = '工程津贴'
        jj_assocs['技术输出 '] = '技术输出'

        return gz_assocs,jj_assocs    


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
        self.datas['sap'] = list()

    def loaddatas(self):

        # 读取工资模板
        gzs, _ = self.batchloaddata(self.conf.get_tpl_root_folder_name(),1,False,'gz')
        # gz_tpl_path = self.get_file_path(self.conf.get_tpl_gz_filename())
        # gzs, _ = self.loaddata(gz_tpl_path, 1, False, 'gz')
        if len(gzs) > 0:
            self.datas['gz'] = gzs
        # 读取奖金模板
        jjs, _ = self.batchloaddata(self.conf.get_tpl_root_folder_name(),1,False,'jj')
        # jj_tpl_path = self.get_file_path(self.conf.get_tpl_jj_filename())
        # jjs, _ = self.loaddata(jj_tpl_path, 1, False, 'jj')
        if len(jjs) > 0:
            self.datas['jj'] = jjs
        # 读取银行卡号
        yhks, _ = self.batchloaddata(self.conf.get_tpl_root_folder_name(),1,False,'yhk')
        # yhk_tpl_path = self.get_file_path(self.conf.get_tpl_yhk_filename())
        # yhks, _ = self.loaddata(yhk_tpl_path, 1, False, 'yhk')
        if len(yhks) > 0:
            self.datas['yhk'] = yhks
        # 读取SAP数据
        saps,_ = self.batchloaddata(self.conf.get_tpl_root_folder_name(),1,False,'sap')
        # sap_tpl_path = self.get_file_path(self.conf.get_tpl_sap_filename())
        # saps, _ = self.loaddata(sap_tpl_path, 1, False, 'sap')
        if len(saps) > 0:
            self.datas['sap'] = saps
        return self.merge_valdator()

    # 验证
    def merge_valdator(self):
        key_col_name = self.conf.get_tpl_map_key_column_name()
        gz_map = self.to_map(self.datas['gz'], key_col_name)
        jj_map = self.to_map(self.datas['jj'], key_col_name)
        yhk_map = self.to_map(self.datas['yhk'], key_col_name)
        sap_map = self.to_map(self.datas['sap'],'员工编号',self.conv_key)

        errs = list()
        errs.extend(self.valdate(gz_map,yhk_map,'gz'))
        errs.extend(self.valdate(jj_map,yhk_map,'jj'))
        if len(sap_map)>0:
            errs.extend(self.valdate_sap(gz_map,jj_map,yhk_map,sap_map))
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
            # 增加按照二级机构切分得逻辑
            for err in sorted(errs):
                with open(err_file, 'a') as f:
                    f.write(err)
                    f.write('\n')

    

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

    
    def valdate_sap(self,gz_map,jj_map,yhk_map,sap_map):
        gz_keys = set(gz_map.keys())
        jj_keys = set(jj_map.keys())
        merge_keys = gz_keys.union(jj_keys)
        sap_keys = set(sap_map.keys())
        errs = list()
        for k in merge_keys:
            vv = gz_map.get(k)
            if vv is None or len(vv) == 0:
                vv = jj_map.get(k)
            if k not in sap_keys:
                errs.append(self.get_err_message(vv,f'无法找到对应得SAP系统数据'))
            else:
                yf = 0
                sf = 0
                if k in gz_map:
                    gz_v = gz_map.get(k)
                    gz_yf_item = self.get_item_by_colname(gz_v[0], '应发')
                    gz_sf_item = self.get_item_by_colname(gz_v[0], '实发')
                    gz_db_item = self.get_item_by_colname(gz_v[0],'独生子女费')
                    gz_jyjf_item = self.get_item_by_colname(gz_v[0],'兼课带教费')
                    if gz_yf_item is not None:
                        yf += gz_yf_item.val
                        if gz_db_item.typ == 2:
                            if gz_db_item.val !='':
                                yf += gz_db_item.val
                        sf += gz_sf_item.val  
                        if gz_db_item.typ == 2:
                            if gz_jyjf_item.val !='':
                                sf -= gz_jyjf_item.val 
                if k in jj_map:
                    jj_v = jj_map.get(k)
                    jj_yf_item = self.get_item_by_colname(jj_v[0], '应发')
                    jj_sf_item = self.get_item_by_colname(jj_v[0],'实发')
                    if jj_yf_item is not None:
                        yf += jj_yf_item.val
                        sf += jj_sf_item.val
                sap_v = sap_map.get(k)
                sap_yf = 0
                sap_sf = 0
                sap_yf_item =  self.get_item_by_colname(sap_v[0], '工资应发')
                sap_ft_item =  self.get_item_by_colname(sap_v[0], '年底兑现奖')
                sap_sf_item =  self.get_item_by_colname(sap_v[0], '实发工资')     
                if  sap_yf_item is not None:
                    sap_yf += sap_yf_item.val + sap_ft_item.val
                    sap_sf += sap_sf_item.val
                
                if round(yf-sap_yf,2) != 0:
                    errs.append(self.get_err_message(vv,f'应发合计不匹配----宝武EHR数值：{yf},SAP数值{sap_yf}'))
                    # 验证 明细
                    gz_vv = None
                    jj_vv = None
                    sap_vv = None
                    if k in gz_map:
                        gz_vv = gz_map.get(k)[0]
                    if k in jj_map:
                        jj_vv = jj_map.get(k)[0]
                    if k in sap_map:
                        sap_vv = sap_map.get(k)[0]
                    errs.extend(self.valdate_sap_detail(vv,sap_map.get(k),gz_vv,jj_vv,sap_vv))
                    # 
                if round(sf-sap_sf,2) != 0:
                    errs.append(self.get_err_message(vv,f'实发合计不匹配----宝武EHR数值：{sf},SAP数值{sap_sf}'))

                # 银行卡验证 
                sap_gz_yhk_item =  self.get_item_by_colname(sap_v[0], '银行卡1')
                sap_jj_yhk_item =  self.get_item_by_colname(sap_v[0], '银行卡2')
                
                yhks = yhk_map.get(k)
                if yhks is not None:
                    gz_yhk  = self.get_yhk_no(yhks,'gz').strip()
                    jj_yhk  = self.get_yhk_no(yhks,'jj').strip()
                    if sap_jj_yhk_item.val == '':
                        sap_jj_yhk_item = sap_gz_yhk_item
                    if sap_gz_yhk_item is not None:
                        if gz_yhk != sap_gz_yhk_item.val:
                            errs.append(self.get_err_message(vv,f'工资卡信息不匹配----宝武EHR数值：{gz_yhk},SAP数值{sap_gz_yhk_item.val}'))
                        if jj_yhk != sap_jj_yhk_item.val:
                            errs.append(self.get_err_message(vv,f'奖金卡信息不匹配----宝武EHR数值：{jj_yhk},SAP数值{sap_jj_yhk_item.val}'))
        
        for v in sap_keys:
            if v not in merge_keys:
                errs.append(self.get_err_message_sap(sap_map.get(v),f'无法找到对应得宝武EHR系统数据'))
        
            
        # 验证应发
        
        # 验证实发
        
        # 验证扣缴  

        return errs

    def valdate_sap_detail(self,vv,sap_vv,gz_v,jj_v,sap_v):
        errs = list()
        gz_as,jj_as = self.item_association()
        for k,v in gz_as.items():
            self.validate_sap_item_detail(vv,sap_vv,gz_v, sap_v,k,v,errs)
        for k,v in jj_as.items():
            self.validate_sap_item_detail(vv,sap_vv,jj_v, sap_v,k,v,errs)
        return errs

    def validate_sap_item_detail(self,vv,sap_vv,gz_v,sap_v,sap_item_name,item_name,errs):
        item = None
        sap_item = None
        if gz_v is not None :
            item = self.get_item_by_colname(gz_v, item_name)
        if sap_v is not None:
            sap_item = self.get_item_by_colname(sap_v, sap_item_name)
        
        if item is not None and item.val!=0 and sap_item is None:
            errs.append(self.get_err_message(vv,f'{item_name}[sap名称{sap_item_name}]不匹配----宝武EHR数值：{item.val},SAP不存在'))
            return
        if item is not None and item.val != sap_item.val:
            if item.val == '' and sap_item.val==0:
                return
            if item.val ==0 and sap_item.val == '':
                return 
            errs.append(self.get_err_message(vv,f'{item_name}[sap名称{sap_item_name}]不匹配----宝武EHR数值：{item.val},SAP数值{sap_item.val}'))
            return
        if item is None and sap_item is not None  and sap_item.val!=0:
            errs.append(self.get_err_message_sap(sap_vv,f'{item_name}[sap名称{sap_item_name}]不匹配----宝武EHR不存在,SAP数值{sap_item.val}'))
            return 

    
    




   

