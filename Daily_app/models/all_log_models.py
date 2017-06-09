#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.


class ChangeHostPass(models.Model):
    '''
    修改服务器密码
    '''
    user_name = models.CharField(u"用户", max_length=120, blank=True, null=True)
    ip_list = models.TextField(u"操作IP", blank=True, null=True)
    add_time = models.CharField(u"变更时间", max_length=120, blank=True, null=True)
    change_re = models.CharField(u"修改状态", max_length=32, blank=True, null=True)

    def __unicode__(self):
        return self.user_name

    class Meta:
        verbose_name_plural = "修改服务器密码"















