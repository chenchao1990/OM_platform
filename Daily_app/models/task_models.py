#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.


class TaskData(models.Model):
    '''
    值班排表
    '''
    date_str = models.CharField(u"日期", max_length=32, blank=True, null=True)
    week_str = models.CharField(u"星期", max_length=16, blank=True, null=True)
    dba_user = models.CharField(u"DBA", max_length=120, blank=True, null=True)
    dba_tel = models.CharField(u"DBA电话", max_length=48, blank=True, null=True)
    sa_user = models.CharField(u"SA", max_length=120, blank=True, null=True)
    sa_tel = models.CharField(u"SA电话", max_length=48, blank=True, null=True)
    month_num = models.IntegerField(u'月份', blank=True, null=True)
    day_num = models.CharField(u'day', max_length=10, blank=True, null=True)
    office_place = models.CharField(u'值班地点', max_length=32, blank=True, null=True)

    def __unicode__(self):
        return u'%s %s %s %s' % (self.date_str, self.dba_user, self.sa_user, self.month_num)

    class Meta:
        verbose_name_plural = "值班排表"


class ImportPassLog(models.Model):
    '''
    导入密码日志表
    '''

    import_type = models.CharField(u"操作类型", max_length=32, blank=True, null=True)
    user_name = models.CharField(u"用户", max_length=64, blank=True, null=True)
    ip_list = models.TextField(u"操作IP", blank=True, null=True)
    re_state = models.CharField(u"导入状态", max_length=16, blank=True, null=True)
    add_time = models.CharField(u"变更时间", max_length=64, blank=True, null=True)

    def __unicode__(self):
        return self.user_name

    class Meta:
        verbose_name_plural = "密码导入记录"


class CloudHosts(models.Model):
    '''
    公司云主机数量
    '''

    another_name = models.CharField(u"别名", max_length=64, blank=True, null=True)
    company = models.CharField(u"公司名称", max_length=128, blank=True, null=True)
    host_count = models.CharField(u"云主机数量", max_length=12, blank=True, null=True)

    def __unicode__(self):
        return self.company

    class Meta:
        verbose_name_plural = "公司云主机数量"


class CloudHostsCount(models.Model):
    '''
    各公司云主机数量
    '''

    another_name = models.CharField(u"别名", max_length=64, blank=True, null=True)
    company = models.CharField(u"公司名称", max_length=128, blank=True, null=True)
    host_count = models.CharField(u"云主机数量", max_length=12, blank=True, null=True)

    def __unicode__(self):
        return self.company

    class Meta:
        verbose_name_plural = "公司云主机数量"














