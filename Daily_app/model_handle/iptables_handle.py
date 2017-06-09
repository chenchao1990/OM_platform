#!/usr/bin/env python
# _*_coding:utf-8 _*_

from Daily_app.models import iptables_models


def get_all_rules():
    values = ['id', 'rule']
    ret = iptables_models.IptablesInit.objects.all().values(*values)
    return ret


def get_rules_by_ids(id_list):
    ret = iptables_models.IptablesInit.objects.filter(id__in=id_list)
    return ret


def get_quick_rule(tag):
    ret = iptables_models.IptablesQuick.objects.filter(tag=tag).first()
    return ret


def iptables_init_log(log_dict):
    '''
    iptables初始化创建日志
    '''
    ret = iptables_models.IptablesLog.objects.create(**log_dict)
    return ret


def get_log_lists_count():
    '''
    获取日志总条数
    :return:
    '''

    ret = iptables_models.IptablesLog.objects.all().count()
    return ret


def get_log_list(start, end, values):
    ret = iptables_models.IptablesLog.objects.all().order_by('-id').values(*values)[start:end]
    return ret








