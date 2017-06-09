#!/usr/bin/env python
# _*_coding:utf-8 _*_

from __future__ import unicode_literals
from django.db import models


class PurchaseBudget(models.Model):
    '''
    采购预算表
    '''

    project_name = models.CharField(u"项目名称",  max_length=120, blank=True, null=True)
    department = models.ForeignKey(u"Department",  blank=True, null=True, verbose_name=u'部门')
    duty_person = models.CharField(u"负责人",  max_length=64, blank=True, null=True)
    new_project = models.CharField(u"新项目",  max_length=12, blank=True, null=True)
    device_model = models.CharField(u"设备型号",  max_length=32, blank=True, null=True)
    plan_phy_quantity = models.CharField(u"评估物理数量",  max_length=12, blank=True, null=True)
    field_1 = models.CharField(u"未知字段1",  max_length=12, blank=True, null=True)
    field_2 = models.CharField(u"未知字段2",  max_length=12, blank=True, null=True)
    budget_unit_price = models.CharField(u"预算单价",  max_length=12, blank=True, null=True)
    budget_count = models.CharField(u"预算数量",  max_length=12, blank=True, null=True)
    budget_total_price = models.CharField(u"预算总金额",  max_length=12, blank=True, null=True)
    vm_configure = models.CharField(u"VM配置",  max_length=24, blank=True, null=True)
    vm_count = models.CharField(u"VM数量",  max_length=12, blank=True, null=True)
    q1_purchase = models.CharField(u"Q1采购",  max_length=10, blank=True, null=True)
    project_approval_state = models.CharField(u"项目立项情况",  max_length=32, blank=True, null=True)
    conf_set_meal = models.CharField(u"配置套餐",  max_length=32, blank=True, null=True)
    raise_conf = models.CharField(u"增加配件",  max_length=32, blank=True, null=True)
    link_up_conf = models.CharField(u"沟通配置",  max_length=120, blank=True, null=True)
    true_time = models.CharField(u"确认时间",  max_length=32, blank=True, null=True)
    true_person = models.CharField(u"确认人",  max_length=16, blank=True, null=True)
    comments = models.TextField(u"备注", blank=True, null=True)

    def __unicode__(self):
        return self.project_name

    class Meta:
        verbose_name_plural = "采购预算表"


class Department(models.Model):
    '''
    部门表
    '''
    name = models.CharField(u"部门名称",  max_length=64, blank=True, null=True)
    cn_name = models.CharField(u"标识",  max_length=32, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "部门"