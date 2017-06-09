#!/usr/bin/env python
# _*_coding:utf-8 _*_

from ansible_app import models


def create_ansible_action_log(data_dict):
    ret = models.AnsibleAPILog.objects.create(**data_dict)
    return ret
