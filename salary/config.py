#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   config.py
@Time    :   2020/08/20 13:49:27
@Author  :   Tong tan 
@Version :   1.0
@Contact :   raogx.vip@hotmail.com
'''


from salary import contants
from dynaconf import Dynaconf


settings = Dynaconf(
    settings_files=['salary/settings.toml'],
    load_dotenv=True,
)

class SalaryConfig(object):
    '''统一管理系统配置信息

    confDict：设置参数字典

    '''
    def __init__(self,confDict:type(dict)=None):
        self._confs = confDict or self.default_settings()

    def default_settings(self) -> dict:
       
        conf = {}
        for k,v in settings.as_dict().items():
            conf[k.lower()] = v
        return conf

    def __get_config_dict(self):
        '''返回所有已配置参数信息
        '''
        return self._confs

    def get_config_val(self,key):
        '''返回配置信息值
        '''
        if not key in self._confs:
            raise KeyError(f'配置项{key}不存在')
        return self.__get_config_dict().get(key)

    
    def contains(self,key):
        return key in self._confs
    
    def config_size(self):
        return len(self._confs)


    def get_pro_name(self):
        return self.get_config_val(contants.PRO_NAME_KEY_NAME)
    
    def get_logging_name(self):
        return self.get_config_val(contants.LOGGING_NAME_KEY_NAME)

    
    def get_logging_level(self):
        return self.get_config_val(contants.LOGGING_LEVEL_KEY_NAME)

    def get_tpl_gz_filename(self):
        return self.__get_tpl_filename(contants.TPL_GZ_FILENAME_KEY_NAME,contants.TPL_GZ_FILENAME_EXT_KEY_NAME)
    
    def get_tpl_jj_filename(self):
        return self.__get_tpl_filename(contants.TPL_JJ_FILENAME_KEY_NAME,contants.TPL_JJ_FILENAME_EXT_KEY_NAME)

    
    def get_tpl_yhk_filename(self):
        return self.__get_tpl_filename(contants.TPL_YHK_FILENAME_KEY_NAME,contants.TPL_YHK_FILENAME_EXT_KEY_NAME)

    def get_tpl_sap_filename(self):
        return self.__get_tpl_filename(contants.TPL_SAP_FILENAME_KEY_NAME,contants.TPL_SAP_FILENAME_EXT_KEY_NAME)
    
    def __get_tpl_filename(self,filename,flieext):
         return f'{self.get_config_val(filename)}.{self.get_config_val(flieext)}'

    def get_tpl_root_folder_name(self):
        return self.get_config_val(contants.TPL_ROOT_FOLDER_NAME_KEY_NAME)

    def get_tpl_map_key_column_name(self):
        return self.get_config_val(contants.TPL_MAP_KEY_COLUMN_NAME_KEY_NAME)   

    def get_tpl_code_column_name(self):
        return self.get_config_val(contants.TPL_CODE_COLUMN_NAME_KEY_NAME) 

    def get_tpl_name_column_name(self):
        return self.get_config_val(contants.TPL_NAME_COLUMN_NAME_KEY_NAME) 

    def get_tpl_depart_column_name(self):
        return self.get_config_val(contants.TPL_DEPART_COLUMN_NAME_KEY_NAME)
    
    def get_tpl_depart_other_column_name(self):
        return self.get_config_val(contants.TPL_DEPART_COLUMN_OTHER_NAME_KEY_NAME)

    def get_bw_code_from_sap_code(self,sap_code):
        items = dict()
        # 马道局
        items['200658'] = 'MA7333'
        # 张朕
        items['200121'] = 'MA7009'
        # 刘轩
        items['45000448'] = 'MA7023'
        if sap_code in items:
            return items.get(sap_code)
        else:
            if len(sap_code)>0 and  len(sap_code) <= 5: 
                return 'M%05d' % int(sap_code)
            return sap_code
    
    
