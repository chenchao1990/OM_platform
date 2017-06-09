#!/usr/bin/env python
# _*_coding:utf-8 _*_

from Daily_app.models import task_models


def password_log_create(data_dict):
    '''
    新增一条导入密码的数据
    '''

    ret = task_models.ImportPassLog.objects.create(**data_dict)
    return ret


def get_pass_log_count():
    '''
    获取密码日志的条数
    '''
    ret = task_models.ImportPassLog.objects.all().count()
    return ret


def get_pass_log_list(start, end, values):
    '''
    获取密码日志的数据
    '''
    ret = task_models.ImportPassLog.objects.all().order_by('-id').values(*values)[start:end]
    return ret
