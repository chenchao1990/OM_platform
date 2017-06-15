#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class CompanyInfo(models.Model):
    '''
    公司名
    '''

    company_name = models.CharField('公司名称', max_length=128,  blank=True, null=True)
    alias_name = models.CharField('别名', max_length=64,  blank=True, null=True)

    def __unicode__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = "云主机公司名称"


class CloudHostCounts(models.Model):
    '''
    各个公司的云主机数量
    '''

    company_id = models.ForeignKey('CompanyInfo', blank=True, null=True)
    add_year = models.CharField('year', max_length=4, blank=True, null=True)
    add_month = models.CharField('month', max_length=4, blank=True, null=True)
    add_week = models.CharField('week', max_length=4, blank=True, null=True)
    add_day = models.CharField('day', max_length=4, blank=True, null=True)
    host_counts = models.CharField('主机数量', max_length=10, null=True, default=0)
    time_md5 = models.CharField('时间戳md5', max_length=24, null=True, blank=True)
    add_time = models.DateTimeField(blank=True, auto_now_add=True)

    def __unicode__(self):
        return u'%s %s' % (self.company_id.company_name, self.host_counts)

    class Meta:
        verbose_name_plural = "云主机数量"

