#!/usr/bin/env python
# _*_coding:utf-8 _*_


from IDC_app import models


def search_data_by_sn(Q, values):
    ret = models.IDCPhysical.objects.filter(Q).values(*values)   # 将总的Q对象添加到model的查找条件中
    return ret


def get_pro_type_list(values):
    ret = models.ProjectType.objects.all().values(*values)
    return ret
