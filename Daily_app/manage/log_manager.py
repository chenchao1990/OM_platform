#!/usr/bin/env python
# _*_coding:utf-8 _*_

from Daily_app.model_handle import log_handle
from overall.response.base_response import BaseResponse
from OM_platform.settings import now_time


def import_password_log(user, ip_list, re_state, import_type):
    '''
    用户操作的IP 写入密码导入日志表中
    '''
    log_dict = {'user_name': None, 'ip_list': None, 'add_time': None, 're_state': re_state, 'import_type': import_type}
    ip_str = ", ".join(ip_list)
    log_dict['user_name'] = user
    log_dict['ip_list'] = ip_str
    log_dict['add_time'] = now_time()
    log_handle.password_log_create(log_dict)


def get_pass_log_count():
    '''
    获取iptables日志总条数
    '''

    response = BaseResponse()
    try:
        result = log_handle.get_pass_log_count()
        response.data = result
        response.status = True
    except Exception, e:
        response.message = str(e)

    return response


def pass_log_data_list(page_start, page_stop):
    '''
    获取指定条数的日志记录
    '''
    response = BaseResponse()
    try:
        values = ['id', 'import_type', 'user_name', 'ip_list', 're_state',  'add_time']      # 在这里定义好查询表时 需要筛选的字段

        result = log_handle.get_pass_log_list(page_start, page_stop, values)                    # 搜索工单信息
        result = list(result)
        response.data = result                                                                  # 封装到对象中
        response.status = True
    except Exception, e:
        response.message = str(e)

    return response









