#!/usr/bin/env python
# _*_coding:utf-8 _*_

from overall.response.base_response import BaseResponse
from Daily_app.model_handle import cloud_host_handle
import datetime


def get_all_host_data():
    response = BaseResponse()
    try:
        d = datetime.datetime.now()

        all_data_list = cloud_host_handle.get_all_data(d.month)
        response.data = list(all_data_list)
        response.month = d.month
        response.status = True
    except Exception, e:
        response.message = e
    return response


def get_all_company():
    '''
    获取所有的公司名称 公司id
    :return:
    '''
    response = BaseResponse()
    try:
        all_company = cloud_host_handle.get_all_company()
        response.status = True
        response.data = list(all_company)
    except Exception, e:
        response.message = e
    return response


def add_new_cloud_data(data):
    '''
    添加新的数据
    '''
    response = BaseResponse()
    try:
        for i, v in data.items():
            if not v:
                return
        data_list = [{'company_id_id': i, 'host_counts': value} for i, value in data.items()]
        cloud_host_handle.add_new_cloud_data(data_list)
        response.status = True
    except Exception, e:
        response.message = e
        print "add  eeeeeeeeeeeeeeeeeeee", e
    return response


def add_new_company(data):
    '''
    添加一个新公司
    :param data:
    :return:
    '''
    response = BaseResponse()
    try:
        data = dict(data)
        alias_name = data.get("alias_name", None)
        print "alias_name>>>>>>>>>>>>>>>", alias_name
        if not alias_name[0]:
            return
        num = cloud_host_handle.get_company(alias_name[0].strip())
        if num > 0:
            return
        data['alias_name'] = data['alias_name'][0].strip()
        data['company_name'] = data['company_name'][0].strip()
        print "ddddddddddddddata", data
        cloud_host_handle.add_new_company(data)
        response.status = True
    except Exception, e:
        response.message = e
        print "add  eeeeeeeeeeeeeeeeeeee", e
    return response
