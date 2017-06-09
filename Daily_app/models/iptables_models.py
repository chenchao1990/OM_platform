#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.


class IptablesInit(models.Model):
    '''
    初始化iptables
    '''
    rule = models.CharField(u"规则", max_length=120, blank=False, null=False)
    belong = models.ForeignKey('IptablesBelong', blank=True, null=True)

    def __unicode__(self):
        return self.rule

    class Meta:
        verbose_name_plural = "iptables初始化规则"


class IptablesBelong(models.Model):
    '''
    iptables所属的环境
    '''
    name = models.CharField(u"环境", max_length=120, blank=False, null=False)
    tag = models.CharField(u"标签", max_length=120, blank=True, null=True)

    def __unicode__(self):
        return self.tag

    class Meta:
        verbose_name_plural = "iptables所属环境"


class IptablesQuick(models.Model):
    '''
    iptables快速插入的规则
    '''
    rule_str = models.CharField(u"规则模板", max_length=120, blank=False, null=False)
    tag = models.CharField(u"类型", max_length=120, blank=True, null=True)

    def __unicode__(self):
        return self.rule_str

    class Meta:
        verbose_name_plural = "快速插入规则模板"


class LogType(models.Model):
    '''
    log type
    '''
    type_name = models.CharField(u"类型", max_length=60, blank=True, null=True)

    def __unicode__(self):
        return self.type_name

    class Meta:
        verbose_name_plural = "日志类型"


class IptablesLog(models.Model):
    '''
    iptables LOG
    '''

    log_type = models.ForeignKey('LogType')
    login_user = models.CharField(u"用户", max_length=120, blank=True, null=True)
    user_num = models.IntegerField(u'用户ID')
    msg = models.TextField(u'日志信息', blank=True, null=True)
    add_time = models.CharField(u"变更时间", max_length=120, blank=True, null=True)
    time_str = models.CharField(u"时间戳", max_length=120, blank=True, null=True)

    def __unicode__(self):
        return u'%s %s %s ' % (self.login_user, self.log_type, self.msg)

    class Meta:
        verbose_name_plural = "Iptables日志"



















