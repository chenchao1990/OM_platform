#!/usr/bin/env python
# _*_coding:utf-8 _*_

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class AnsibleAPILog(models.Model):
    '''
    执行命令日志
    '''
    action_type = models.CharField(u"操作类型", max_length=32, blank=True, null=True)
    user_name = models.CharField(u"用户", max_length=32, blank=True, null=True)
    shell_str = models.TextField(u"执行的命令", blank=True, null=True)
    action_ips = models.TextField(u"操作的IP", blank=True, null=True)
    file_name = models.CharField(u"文件名", max_length=64, blank=True, null=True)
    script_name = models.CharField(u"脚本名", max_length=64, blank=True, null=True)
    add_time = models.CharField(u"时间", max_length=32, blank=True, null=True)

    def __unicode__(self):
        return self.user_name

    class Meta:
        verbose_name_plural = "ansible操作日志"
