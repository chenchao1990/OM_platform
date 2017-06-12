#!/usr/bin/env python
# _*_coding:utf-8 _*_

from overall.response.base_response import BaseResponse
from Daily_app.model_handle import cloud_host_handle


def get_all_host_data():
    response = BaseResponse()
    try:

        all_data_list = cloud_host_handle.get_host_data()
        print "alllllllllllllllllll", all_data_list
        response.data = list(all_data_list)
        response.status = True
    except Exception, e:
        response.message = e
    return response
