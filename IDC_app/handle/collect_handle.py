#!/usr/bin/env python
# _*_coding:utf-8 _*_

from IDC_app import models


def get_all_apply_type():
    # 获取所有的应用类型服务器个数
    try:
        ret = models.IDCPhysical.objects.all().values("app_type").exclude(app_type__in=[" "]).count()
        return ret
    except Exception, e:
        print "eeeeeeeeeeeee", e


def get_all_sql():
    # 获取所有数据库的个数
    ret = models.IDCPhysical.objects.filter(app_type=u"数据库").count()
    return ret


def get_all_app():
    # 获取所有应用的个数
    ret = models.IDCPhysical.objects.filter(app_type=u"应用").count()
    return ret


def get_all_app_virtual():
    # 获取所有应用宿主机的个数
    ret = models.IDCPhysical.objects.filter(server_type=u"宿主机").count()
    return ret


def get_all_app_no_virtual():
    # 获取所有应用非宿主机的个数
    ret = models.IDCPhysical.objects.filter(server_type=u"非宿主机").count()
    return ret


def get_no_user_device_status():
    # 获取所有下线报废的数量
    ret = models.IDCPhysical.objects.filter(device_status__in=[u"下线", u"报废"]).count()
    return ret


def get_all_vhost_online():
    # 获取所有宿主机、在线的数量
    ret = models.IDCPhysical.objects.filter(server_type=u"宿主机", device_status=u"在线").count()
    return ret


def get_all_host_online():
    # 获取所有非宿主机、在线的数量
    ret = models.IDCPhysical.objects.filter(server_type=u"非宿主机", device_status=u"在线").count()
    return ret


def get_all_host_downline():
    # 获取所有非宿主机、下线的数量
    ret = models.IDCPhysical.objects.filter(server_type=u"非宿主机", device_status=u"下线").count()
    return ret


def get_all_vhost_downline():
    # 获取所有宿主机、下线的数量
    ret = models.IDCPhysical.objects.filter(server_type=u"宿主机", device_status=u"下线").count()
    return ret


def get_all_host_not_use():
    # 获取所有非宿主机、报废的数量
    ret = models.IDCPhysical.objects.filter(server_type=u"非宿主机", device_status=u"报废").count()
    return ret


def get_all_vhost_not_use():
    # 获取所有宿主机、报废的数量
    ret = models.IDCPhysical.objects.filter(server_type=u"宿主机", device_status=u"报废").count()
    return ret


def get_can_virtual_online():
    # 获取所有可虚拟化、在线的数量
    ret = models.IDCPhysical.objects.filter(is_virtual=u"是", device_status=u"在线").count()
    return ret


def get_can_virtual_offline():
    # 获取所有可虚拟化、下线的数量
    ret = models.IDCPhysical.objects.filter(is_virtual=u"是", device_status=u"下线").count()
    return ret


def get_can_virtual_scrap():
    # 获取所有可虚拟化、报废的数量
    ret = models.IDCPhysical.objects.filter(is_virtual=u"是", device_status=u"报废").count()
    return ret


def get_not_virtual_online():
    # 获取所有可虚拟化、在线的数量
    ret = models.IDCPhysical.objects.filter(is_virtual=u"否", device_status=u"在线").count()
    return ret


def get_not_virtual_offline():
    # 获取所有可虚拟化、下线的数量
    ret = models.IDCPhysical.objects.filter(is_virtual=u"否", device_status=u"下线").count()
    return ret


def get_not_virtual_scrap():
    # 获取所有可虚拟化、报废的数量
    ret = models.IDCPhysical.objects.filter(is_virtual=u"否", device_status=u"报废").count()
    return ret


def get_idc_device_status(idc_name):
    # 获取各个机房不同状态的设备数量   （在线 下线 报废）
    online = models.IDCPhysical.objects.filter(idc=idc_name, device_status=u"在线").count()
    offline = models.IDCPhysical.objects.filter(idc=idc_name, device_status=u"下线").count()
    scrap = models.IDCPhysical.objects.filter(idc=idc_name, device_status=u"报废").count()
    return online, offline, scrap


def get_brand_status(device_name):
    # 获取各个品牌服务器不同状态的设备数量   （在线 下线 报废）
    online = models.IDCPhysical.objects.filter(brand=device_name, device_status=u"在线").count()
    offline = models.IDCPhysical.objects.filter(brand=device_name, device_status=u"下线").count()
    scrap = models.IDCPhysical.objects.filter(brand=device_name, device_status=u"报废").count()
    return online, offline, scrap






