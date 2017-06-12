#!/usr/bin/env python
# _*_coding:utf-8 _*_

from Daily_app.models.task_models import CloudHosts


def get_host_data():
    '''
    获取所有数据展示到前端
    '''
    ret = CloudHosts.objects.all().values()
    return ret
