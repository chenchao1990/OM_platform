#!/usr/bin/env python
# _*_coding:utf-8 _*_

from OM_platform.settings import now_time
from ansible_app.model_handle import ansible_log_handle


def sql_dict(user, msg, ip_list, action_type):
    data_dict = {'user_name': '', 'shell_str':'', 'action_ips':'', 'file_name':'',
                 'script_name':'', 'add_time': '', 'action_type': action_type}
    data_dict['user_name'] = user
    data_dict['action_type'] = action_type
    data_dict['action_ips'] = ','.join(ip_list)
    if action_type == 'SHELL':
        data_dict['shell_str'] = msg
    elif action_type == 'FILE':
        data_dict['file_name'] = msg
    elif action_type == 'SCRIPT':
        data_dict['script_name'] = msg
    data_dict['add_time'] = now_time()
    return data_dict


def ansible_shell_log(user, ip_list, cmd_str):
    '''
    执行命令的日志
    '''
    data_dict = sql_dict(user, cmd_str, ip_list, 'SHELL')                           # 生成数据字典
    ansible_log_handle.create_ansible_action_log(data_dict)                     # 存入日志表中


def ansible_file_log(user, ip_list, file_name):
    '''
    上传文件的日志
    '''
    data_dict = sql_dict(user, file_name, ip_list, 'FILE')                        # 生成数据字典
    ansible_log_handle.create_ansible_action_log(data_dict)                 # 存入日志表中


def ansible_script_log(user, ip_list, script_name):
    '''
    执行脚本的日志
    '''
    data_dict = sql_dict(user, script_name, ip_list, 'SCRIPT')                          # 生成数据字典
    ansible_log_handle.create_ansible_action_log(data_dict)                     # 存入日志表中



