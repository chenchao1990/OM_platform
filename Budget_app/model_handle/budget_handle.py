#!/usr/bin/env python
# _*_coding:utf-8 _*_

from Budget_app import models
from collections import OrderedDict


def get_all_budget_data():
    ret = models.PurchaseBudget.objects.all()
    return ret


def get_budget_by_department(department_list):
    '''
    根据部门的名称去获取各个部门的项目数据
    '''
    re_list = []

    for name in department_list:
        c_name = models.Department.objects.filter(cn_name=name)[0].name
        ret = list(models.PurchaseBudget.objects.filter(department__cn_name=name).values())
        for i in ret:
            i.pop('department_id')
            i['department'] = c_name
        re_list.append(ret)
    return re_list


def get_all_department_data():
    va = ['cn_name']
    re_name_list = []
    ret = list(models.Department.objects.all().values_list(*va))

    for i in ret:
        re_name_list.append(i[0])
    return re_name_list


def get_all_verb_name():
    verbose_name_dict = OrderedDict()
    ret = models.PurchaseBudget._meta.fields
    for i in ret:
        verbose_name_dict[i.name] = i.verbose_name
    verbose_name_dict.pop('id')
    only_name_list = verbose_name_dict.keys()

    print "only_name_list", only_name_list
    return verbose_name_dict, only_name_list









