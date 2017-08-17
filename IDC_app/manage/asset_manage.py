#!/usr/bin/env python
# _*_coding:utf-8 _*_
from overall.response.base_response import BaseResponse
from django.db.models import Q
from IDC_app.handle import search_handle
from IDC_app.models import IDCPhysical
import json
import re
import xlrd


def get_search_asset(search_data):
    # 根据搜索 获取数据

    response = BaseResponse()
    try:
        print "input___________search_data", search_data
        if search_data:
            values = ["id", "pro_type", "ip", "device_type", "server_type", "app_type", "device_status", "is_virtual",
                      "sn", "brand", "own_person", "idc", "cabinet"]
            q1 = Q()
            q1.connector = 'OR'      # q1的元素为OR或的关系
            q1.children.append(('sn', search_data))
            ret = search_handle.search_data_by_sn(q1, values)
            print "serach______data", ret

            response.data = list(ret)
            response.status = True

    except Exception, e:
        print "eeeeeeeeeeeeeeeeeeerror", e
        response.message = str(e)
    return response


def get_all_pro_type():
    response = BaseResponse()
    try:
        values = ['id', 'name', ]
        result = search_handle.get_pro_type_list(values)         # 返回的是一个类似列表
        result = list(result)                           # 转换为list类型
        print "pro_____type", result
        response.data = result                          # 封装到对象中
        response.status = True
    except Exception, e:
        response.message = str(e)
    return response                                     # 将封装设备状态数据的对象返回
