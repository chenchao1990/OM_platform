#!/usr/bin/env python
# _*_coding:utf-8 _*_
from overall.response.base_response import IDCResponse
from overall.response.base_response import BaseResponse
from IDC_app.handle import collect_handle
import json


def data_percent(a, b):
    s = float(a) / b
    return "%.2f%%" % (s * 100)


# 将收集到的数据合并 返回
def collect_all_data():
    response = IDCResponse()
    try:
        sql = sql_data().__dict__            # 获取数据库与应用的数据
        response.sql_and_app = sql

        vhost_host = host_vhost().__dict__      # 获取宿主机 非宿主机数据
        response.vir_host = vhost_host

        virtual_not_vir = virtual_can_not_virtual().__dict__        # 可虚拟化与不可虚拟化
        response.can_virtual = virtual_not_vir

        idc_info = idc_info_data().__dict__             # idc的设备各种状态信息
        response.idc = idc_info

        bran_info = brand_data().__dict__               # 各个服务器品牌不同状态信息
        response.brand = bran_info

        response.status = True
    except Exception, e:
        response.message = e.message
    return response


# 数据库与应用的统计信息
def sql_data():
    response = BaseResponse()
    try:
        ret = {}
        all_app_type_count = collect_handle.get_all_apply_type()            # 所有应用类型的个数
        all_sql_count = collect_handle.get_all_sql()                        # 所有数据库个数
        all_app_virtual = collect_handle.get_all_app_virtual()              # 应用宿主机
        all_app_no_virtual = collect_handle.get_all_app_no_virtual()        # 应用非宿主机
        all_device_can_not_use = collect_handle.get_no_user_device_status()     # 获取下线报废的个数
        all_count = all_sql_count + all_app_virtual + all_app_no_virtual + all_device_can_not_use
        sql_percent = data_percent(all_sql_count, all_app_type_count - all_device_can_not_use)
        app_percent = data_percent(all_app_virtual, all_count-all_device_can_not_use)

        # ret['all_app_type_count'] = all_app_type_count
        # ret['all_app_count'] = all_app_count
        ret['all_sql_count'] = all_sql_count
        ret['all_app_virtual'] = all_app_virtual
        ret['all_app_no_virtual'] = all_app_no_virtual
        ret['all_device_can_not_use'] = all_device_can_not_use
        ret['all_count'] = all_count
        ret['sql_percent'] = sql_percent
        ret['app_percent'] = app_percent

        response.data = ret
        response.status = True
    except Exception, e:
        response.message = e.message

    return response


# 宿主机与非宿主机比率
def host_vhost():
    response = BaseResponse()
    try:
        ret = {}
        all_vhost_online = collect_handle.get_all_vhost_online()            # 宿主机、在线
        all_vhost_downline = collect_handle.get_all_vhost_downline()        # 宿主机、下线
        all_vhost_not_use = collect_handle.get_all_vhost_not_use()          # 宿主机、报废
        all_host_online = collect_handle.get_all_host_online()              # 非宿主机、在线
        all_host_downline = collect_handle.get_all_host_downline()          # 非宿主机、下线
        all_host_not_use = collect_handle.get_all_host_not_use()            # 非宿主机、报废
        all_vhost_count = all_vhost_online + all_vhost_downline + all_vhost_not_use
        all_host_count = all_host_online + all_host_downline + all_host_not_use
        online_count = all_vhost_online + all_host_online               # 在线的数量
        down_line_count = all_vhost_downline + all_host_downline        # 下线的数量
        all_count = all_vhost_count + all_host_count                    # 所有的机器
        vhost_percent = data_percent(all_vhost_online, all_count)       # 宿主机占比
        host_percent = data_percent(all_host_online, all_count)         # 非宿主机占比

        ret['all_vhost_online'] = all_vhost_online
        ret['all_vhost_downline'] = all_vhost_downline
        ret['all_vhost_not_use'] = all_vhost_not_use
        ret['all_host_online'] = all_host_online
        ret['all_host_downline'] = all_host_downline
        ret['all_host_not_use'] = all_host_not_use
        ret['all_vhost_count'] = all_vhost_count
        ret['all_host_count'] = all_host_count
        ret['online_count'] = online_count
        ret['down_line_count'] = down_line_count
        ret['all_count'] = all_count
        ret['vhost_percent'] = vhost_percent
        ret['host_percent'] = host_percent

        response.data = ret
        response.status = True
    except Exception, e:
        response.message = e.message

    return response


# 虚拟化与不可虚拟化
def virtual_can_not_virtual():
    response = BaseResponse()
    try:
        ret = {}
        can_virtual_online = collect_handle.get_can_virtual_online()            # 可虚拟化 在线
        can_virtual_offline = collect_handle.get_can_virtual_offline()          # 可虚拟化 下线
        can_virtual_scrap = collect_handle.get_can_virtual_scrap()              # 可虚拟化 报废

        not_virtual_online = collect_handle.get_not_virtual_online()            # 不可虚拟化 在线
        not_virtual_offline = collect_handle.get_not_virtual_offline()          # 不可虚拟化 在线
        not_virtual_scrap = collect_handle.get_not_virtual_scrap()              # 不可虚拟化 报废

        all_can_virtual = can_virtual_online + can_virtual_offline + can_virtual_scrap
        all_not_virtual = not_virtual_online + not_virtual_offline + not_virtual_scrap

        ret['can_virtual_online'] = can_virtual_online
        ret['can_virtual_offline'] = can_virtual_offline
        ret['can_virtual_scrap'] = can_virtual_scrap
        ret['not_virtual_online'] = not_virtual_online
        ret['not_virtual_offline'] = not_virtual_offline
        ret['not_virtual_scrap'] = not_virtual_scrap
        ret['all_can_virtual'] = all_can_virtual
        ret['all_not_virtual'] = all_not_virtual

        response.data = ret
        response.status = True
    except Exception, e:
        response.message = e.message

    return response


# 各个机房的信息统计
def idc_info_data():
    response = BaseResponse()
    try:
        ret = []
        all_idc_list = [u"德信", u"M6", u"鹏博士", u"M5", u"大簇"]
        for name in all_idc_list:
            idc_dict = {}
            online, offline, scrap = collect_handle.get_idc_device_status(name)
            idc_dict['name'] = name
            idc_dict['online'] = online
            idc_dict['offline'] = offline
            idc_dict['scrap'] = scrap
            idc_dict['all_count'] = online + offline + scrap
            ret.append(idc_dict)
        response.data = ret
        response.status = True
    except Exception, e:
        response.message = e.message

    return response


# 各个服务器品牌信息统计
def brand_data():
    response = BaseResponse()
    try:
        ret = []
        all_deivce_list = [u"浪潮", u"华为", u"DELL", u"HP", u"曙光", u"IBM"]
        for name in all_deivce_list:
            brand_dict = {}
            online, offline, scrap = collect_handle.get_brand_status(name)
            brand_dict['name'] = name
            brand_dict['online'] = online
            brand_dict['offline'] = offline
            brand_dict['scrap'] = scrap
            brand_dict['all_count'] = online + offline + scrap
            ret.append(brand_dict)
        response.data = ret
        response.status = True
    except Exception, e:
        response.message = e.message

    return response
