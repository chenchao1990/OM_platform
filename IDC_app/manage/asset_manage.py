#!/usr/bin/env python
# _*_coding:utf-8 _*_
from overall.response.base_response import BaseResponse
from django.db.models import Q
from IDC_app.handle import search_handle
import json


def get_search_asset(search_data):
    # 根据搜索 获取数据

    response = BaseResponse()
    try:
        if search_data:
            values = ["id", "pro_type", "ip", "device_type", "server_type", "app_type", "device_status", "is_virtual",
                      "sn", "brand", "own_person", "idc", "cabinet"]
            q1 = Q()
            q1.connector = 'OR'      # q1的元素为OR或的关系
            q1.children.append(('sn', search_data))
            ret = search_handle.search_data_by_sn(q1, values)

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
        response.data = result                          # 封装到对象中
        response.status = True
    except Exception, e:
        response.message = str(e)
    return response                                     # 将封装设备状态数据的对象返回


def update_date(data):
    response = BaseResponse()

    rows = json.loads(data)
    error_count = 0
    error_message = []
    for item in rows:
        try:
            search_handle.update_date_by_id(item)
        except Exception, e:
            error_count += 1
            error_message.append({'message': str(e)})

    if error_count == 0:
        response.status = True
        response.data = "更新%d条,成功%d." % (len(rows), len(rows)-error_count)
    elif error_count > 0:
        response.data = "更新%d条,成功%d,失败%d." % (len(rows), len(rows)-error_count, error_count)
        response.message = error_message

    return response                                     # 将封装设备状态数据的对象返回


def collect_data():
    # 采集一些统计数据
    response = BaseResponse()

    return response























