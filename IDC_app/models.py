# _*_coding:utf-8 _*_

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class IDCPhysical(models.Model):
    # 机房所有的物理机
    pro_type = models.CharField(u"项目类型", max_length=20, blank=True, null=True)
    ip = models.CharField(u"IP地址",  max_length=20, blank=True, null=True)
    device_type = models.CharField(u"设备类型", max_length=20, blank=True, null=True)
    server_type = models.CharField(u"服务类型", max_length=25, blank=True, null=True)
    app_type = models.CharField(u"应用类型", max_length=20, blank=True, null=True)
    device_status = models.CharField(u"设备状态", max_length=12, blank=True, null=True)
    is_virtual = models.CharField(u"是否可虚拟化", max_length=10, blank=True, null=True)
    sn = models.CharField(u"资产编号", max_length=20, blank=True, null=True)
    brand = models.CharField(u"设备品牌", max_length=15, blank=True, null=True)
    device_version = models.CharField(u"设备型号", max_length=50, blank=True, null=True)
    device_conf = models.CharField(u"设备配置", max_length=25, blank=True, null=True)
    own_person = models.CharField(u"所属人", max_length=20, blank=True, null=True)
    pro_line1 = models.TextField(u"产品线1", blank=True, null=True)
    pro_line2 = models.TextField(u"产品线2", blank=True, null=True)
    pro_line3 = models.TextField(u"产品线3", blank=True, null=True)
    pro_person = models.TextField(u"产品线负责人", max_length=16, blank=True, null=True)
    module = models.CharField(u"所属板块", max_length=15, blank=True, null=True)
    idc = models.CharField(u"所在机房", max_length=16, blank=True, null=True)
    cabinet = models.CharField(u"所属机柜", max_length=10, blank=True, null=True)
    cabinet_status = models.CharField(u"机柜状态", max_length=16, blank=True, null=True)
    time_period = models.CharField(u"时间周期", max_length=20, blank=True, null=True)
    delivery_date = models.CharField(u"交付日期", max_length=20, blank=True, null=True)

    def __unicode__(self):
        return "%s %s %s %s %s" % (self.ip, self.pro_type, self.app_type, self.own_person, self.idc)

    class Meta:
        verbose_name_plural = "机房所有物理机"             # 这里设置在admin表周的名称


class ProjectType(models.Model):
    # 项目类型
    name = models.CharField(u"项目名称",  max_length=12, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "项目类型"


class DeviceType(models.Model):
    # 设备类型
    name = models.CharField(u"设备名称",  max_length=15, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "设备类型"


class ServerType(models.Model):
    # 服务类型
    name = models.CharField(u"服务名称",  max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "服务类型"


class AppType(models.Model):
    # 应用类型
    name = models.CharField(u"应用名称",  max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "应用类型"


class DeviceStatus(models.Model):
    # 设备状态
    name = models.CharField(u"状态名称",  max_length=12, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "设备状态"


class IsVirtual(models.Model):
    # 是否可虚拟化
    name = models.CharField(u"是否",  max_length=10, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "是否可虚拟化"


class Brand(models.Model):
    # 设备品牌
    name = models.CharField(u"品牌名称",  max_length=20, blank=True, null=True)
    tag = models.CharField(max_length=15, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "设备品牌"


class DeviceVersion(models.Model):
    # 设备型号
    name = models.CharField(u"设备型号",  max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "设备型号"


class Personal(models.Model):
    # 所属人
    name = models.CharField(u"所属人",  max_length=20, blank=True, null=True)
    tag = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "所属人"


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
    tag = models.CharField(max_length=16, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "产品线负责人"


class Module(models.Model):
    # 所属板块
    name = models.CharField(u"板块名称",  max_length=16, blank=True, null=True)
    tag = models.CharField(max_length=25, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "所属板块"


class IDC(models.Model):
    # 所属机房
    name = models.CharField(u"机房名称",  max_length=16, blank=True, null=True)
    tag = models.CharField(max_length=16, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "所属机房"


class CabinetStatus(models.Model):
    # 机柜状态
    name = models.CharField(u"状态名称",  max_length=16, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "机柜状态"





