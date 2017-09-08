#!/usr/bin/env python
# _*_coding:utf-8 _*_

from django.db import transaction
from IDC_app import models


def search_data_by_sn(Q, values):
    ret = models.IDCPhysical.objects.filter(Q).values(*values)   # 将总的Q对象添加到model的查找条件中
    return ret


def get_pro_type_list(values):
    ret = models.ProjectType.objects.all().values(*values)
    return ret


def get_asset_by_id(asset_id):              # 基于ID去获取数据
    ret = models.IDCPhysical.objects.filter(id=asset_id).first()
    return ret


def delete_data_by_id(asset_id):              # 基于ID去删除数据
    ret = models.IDCPhysical.objects.filter(id=asset_id).delete()
    return ret


def update_date_by_id(data_dict):
    with transaction.atomic():
        asset_obj = get_asset_by_id(data_dict['id'])
        if (data_dict.has_key('pro_type')):
            asset_obj.pro_type = data_dict['pro_type']
        asset_obj.save()


