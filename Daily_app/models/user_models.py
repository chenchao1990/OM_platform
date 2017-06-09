#!/usr/bin/env python
# _*_coding:utf-8 _*_


from __future__ import unicode_literals

from django.db import models


class UserType(models.Model):
    '''
    用户类型
    '''
    caption = models.CharField(u'部门', max_length=32, db_index=True, unique=True)
    code = models.CharField(u'优先级', max_length=32, db_index=True, unique=True)
    msg = models.CharField(u'用户信息', max_length=32, null=True, blank=True)

    def __unicode__(self):
        return self.caption

    class Meta:
        verbose_name_plural = "用户类型"


class UserInfo(models.Model):
    '''
    用户的基本信息
    '''
    user_type = models.ForeignKey('UserType')
    cn_name = models.CharField(u'中文名', max_length=64, blank=False, null=False)
    username = models.CharField(u'username', max_length=64, blank=False, null=False)
    email = models.EmailField(u'邮箱', blank=True, null=True )
    mobile = models.CharField(u'手机', max_length=32, null=True, blank=True)
    task_id = models.IntegerField(u'值班id', null=True, blank=True)
    user_auth = models.IntegerField(u'用户权限', null=True, blank=True)

    class Meta:
        verbose_name_plural = "用户信息"

    def __unicode__(self):
        return self.cn_name


class AdminInfo(models.Model):
    '''
    用户登陆账号
    '''
    user_info = models.OneToOneField('UserInfo')
    username = models.CharField(u'用户名', max_length=256)
    password = models.CharField(u'密码', max_length=256)

    class Meta:
        verbose_name_plural = "用户登陆账号"

    def __unicode__(self):
        return self.user_info


class IptablesAuth(models.Model):
    '''
    iptables登陆验证
    '''
    user = models.CharField(u'用户名', unique=True, max_length=32)
    ip = models.CharField(u'ip地址', max_length=32)
    p_key = models.CharField(u'私钥', max_length=32)

    class Meta:
        verbose_name_plural = "iptables用户验证"

    def __unicode__(self):
        return self.user































