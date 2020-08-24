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
        return f'{self.get_config_val(contants.TPL_GZ_FILENAME_KEY_NAME)}.{self.get_config_val(contants.TPL_GZ_FILENAME_EXT_KEY_NAME)}'

    def get_tpl_root_folder_name(self):
        return self.get_config_val(contants.TPL_ROOT_FOLDER_NAME_KEY_NAME)
