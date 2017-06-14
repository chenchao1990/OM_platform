#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime


def get_week_of_month():
    """
    获取指定的某天是某个月中的第几周
    周一作为一周的开始
    """
    d = datetime.datetime.now()
    end = int(datetime.datetime(d.year, d.month, d.day).strftime("%W"))
    begin = int(datetime.datetime(d.year, d.month, 1).strftime("%W"))
    weekth = end - begin                   # 获取当天是第几周

    return d.year, d.month, d.day, weekth


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
    y, m, d, w = get_week_of_month()
    company_id = models.ForeignKey('CompanyInfo', blank=True, null=True)
    add_year = models.CharField('year', max_length=4, blank=True, null=True, default=y)
    add_month = models.CharField('month', max_length=4, blank=True, null=True, default=m)
    add_week = models.CharField('week', max_length=4, blank=True, null=True, default=w)
    add_day = models.CharField('day', max_length=4, blank=True, null=True, default=d)
    host_counts = models.CharField('主机数量', max_length=10, null=True, default=0)
    add_time = models.DateTimeField(blank=True, auto_now_add=True)

    def __unicode__(self):
        return u'%s %s' % (self.company_id.company_name, self.host_counts)

    class Meta:
        verbose_name_plural = "云主机数量"

