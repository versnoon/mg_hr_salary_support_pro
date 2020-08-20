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
    envvar_prefix="SALARY_SUPPORT",
    settings_files=['salary/settings.toml'],
)


class SalaryConfig(object):
    '''统一管理系统配置信息

    confDict：设置参数字典

    '''
    def __init__(self,confDict:type(dict)=None):
        self._confs = confDict or self.default_settings()

    def default_settings(self) -> dict:
        conf = {}
        # 项目名称
        conf[contants.PRO_NAME_KEY_NAME] = settings.proname
        return conf

    def get_config_dict(self):
        '''返回所有已配置参数信息
        '''
        return self._confs

    def get_config_val(self,key):
        '''返回配置信息值
        '''
        if not key in self._confs:
            raise KeyError(f'配置项{key}不存在')
        return self.get_config_dict().get(key)