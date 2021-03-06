#!/usr/bin/env python
# _*_coding:utf-8 _*_


class BaseResponse(object):
    def __init__(self):
        self.status = False
        self.message = ''
        self.data = None
        self.other = None


class IDCResponse(object):
    def __init__(self):
        self.status = False
        self.message = ''
        self.sql_and_app = None         # 数据库与应用
        self.vir_host = None            # 宿主机与非宿主机
        self.can_virtual = None         # 可虚拟化与不可虚拟化
        self.idc = None                 # 机房
        self.brand = None               # 品牌


class TaskResponse(object):
    def __init__(self):
        self.status = False
        self.message = ''
        self.data = None
        self.current_time = None
        self.current_month = None
        self.current_day = None


class IptablesCheck(object):
    '''
    检测用户输入的内容是否符合规则
    '''
    def __init__(self):
        self.check_status = True
        self.check_result = None
        self.ip_status = True
        self.status = False
        self.pwd_status = True
        self.message = ''
        self.host_ip = None
        self.check_ip = None
        self.rule_list = None
        self.data = None


class AnsibleResponse(object):
    '''
    ansible的执行结果
    '''
    def __init__(self):
        self.status = False
        self.ip_state = True
        self.pwd_state = True
        self.cmd_state = True
        self.message = ''
        self.no_pass = ''
        self.data = None


class BudgetResponse(object):
    def __init__(self):
        self.status = False
        self.message = ''
        self.title_dict = None
        self.title_name = None
        self.budget_data = None
