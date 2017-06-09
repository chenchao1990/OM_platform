#!/usr/bin/env python
# _*_coding:utf-8 _*_

from Daily_app.model_handle import iptables_handle
from OM_platform.settings import now_time
from django.db import transaction
import time


def iptables_init_log(user_name, user_id, ip_list):
    '''
    iptables 初始化创建日志
    '''

    with transaction.atomic():
        ip_str = ','.join(ip_list.strip().split(","))
        new_time = now_time()
        time_str = time.time()
        data_dict = {
                     'log_type_id': '1',
                     'login_user': user_name,
                     'user_num': user_id,
                     'msg': ip_str,
                     'add_time': new_time,
                     'time_str': time_str
                     }
        iptables_handle.iptables_init_log(data_dict)




























