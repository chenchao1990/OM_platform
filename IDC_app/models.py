# _*_coding:utf-8 _*_

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class IDCPhysical(models.Model):
    # 机房所有的物理机
    pro_type = models.ForeignKey('ProjectType', verbose_name=u"项目类型", blank=True, null=True)
    ip = models.CharField(u"IP地址",  max_length=20, blank=True, null=True)
    device_type = models.ForeignKey('DeviceType', verbose_name=u"设备类型", blank=True, null=True)
    server_type = models.ForeignKey('ServerType', verbose_name=u"服务类型", blank=True, null=True)
    app_type = models.ForeignKey('AppType', verbose_name=u"应用类型", blank=True, null=True)
    device_status = models.ForeignKey('DeviceStatus', verbose_name=u"设备状态", blank=True, null=True)
    is_virtual = models.ForeignKey('IsVirtual', verbose_name=u"是否可虚拟化", blank=True, null=True)
    sn = models.CharField(u"资产编号", max_length=20, blank=True, null=True)
    brand = models.ForeignKey('Brand', verbose_name=u"设备品牌", blank=True, null=True)
    device_version = models.ForeignKey('DeviceVersion', verbose_name=u"设备型号", blank=True, null=True)
    device_conf = models.CharField(u"设备配置", max_length=25, blank=True, null=True)
    own_person = models.ForeignKey('Personal', verbose_name=u"所属人", max_length=20, blank=True, null=True)
    pro_line1 = models.ForeignKey('ProductLine1', verbose_name=u"产品线1", blank=True, null=True)
    pro_line2 = models.ForeignKey('ProductLine2', verbose_name=u"产品线2", blank=True, null=True)
    pro_line3 = models.ForeignKey('ProductLine3', verbose_name=u"产品线3", blank=True, null=True)
    pro_person = models.ForeignKey('ProductPerson', verbose_name=u"产品线负责人", blank=True, null=True)
    module = models.ForeignKey('Module', verbose_name=u"所属板块", blank=True, null=True)
    idc = models.ForeignKey('IDC', verbose_name=u"所在机房", blank=True, null=True)
    cabinet = models.CharField(u"所属机柜", max_length=10, blank=True, null=True)
    cabinet_status = models.ForeignKey('CabinetStatus', verbose_name=u"机柜状态", blank=True, null=True)
    time_period = models.CharField(u"时间周期", max_length=20, blank=True, null=True)
    delivery_date = models.CharField(u"交付日期", max_length=20, blank=True, null=True)

    def __unicode__(self):
        return "%s %s %s %s %s" % (self.ip, self.pro_type, self.app_type, self.own_person, self.idc)

    class Meta:
        verbose_name_plural = "机房所有物理机"


class ProjectType(models.Model):
    # 项目类型
    name = models.CharField(u"项目名称",  max_length=12, blank=True, null=True)

    def __unicode__(self):
        return self.name


class DeviceType(models.Model):
    # 设备类型
    name = models.CharField(u"设备名称",  max_length=15, blank=True, null=True)

    def __unicode__(self):
        return self.name


class ServerType(models.Model):
    # 服务类型
    name = models.CharField(u"服务名称",  max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.name


class AppType(models.Model):
    # 应用类型
    name = models.CharField(u"应用名称",  max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.name


class DeviceStatus(models.Model):
    # 设备状态
    name = models.CharField(u"状态名称",  max_length=12, blank=True, null=True)

    def __unicode__(self):
        return self.name


class IsVirtual(models.Model):
    # 是否可虚拟化
    name = models.CharField(u"是否",  max_length=10, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Brand(models.Model):
    # 设备品牌
    name = models.CharField(u"设备品牌",  max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.name


class DeviceVersion(models.Model):
    # 设备型号
    name = models.CharField(u"设备型号",  max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Personal(models.Model):
    # 所属人
    name = models.CharField(u"所属人",  max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.name


class ProductLine1(models.Model):
    # 产品线1
    name = models.CharField(u"产品线1",  max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.name


class ProductLine2(models.Model):
    # 产品线2
    name = models.CharField(u"产品线2",  max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.name


class ProductLine3(models.Model):
    # 产品线3
    name = models.CharField(u"产品线3",  max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.name


class ProductPerson(models.Model):
    # 产品线负责人
    name = models.CharField(u"产品线负责人",  max_length=16, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Module(models.Model):
    # 所属板块
    name = models.CharField(u"所属板块",  max_length=16, blank=True, null=True)

    def __unicode__(self):
        return self.name


class IDC(models.Model):
    # 所属机房
    name = models.CharField(u"所属机房",  max_length=16, blank=True, null=True)

    def __unicode__(self):
        return self.name


class CabinetStatus(models.Model):
    # 机柜状态
    name = models.CharField(u"机柜状态",  max_length=16, blank=True, null=True)

    def __unicode__(self):
        return self.name





