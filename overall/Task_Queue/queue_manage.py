#!/usr/bin/env python
# _*_coding:utf-8 _*_

from RedisQueue import RedisQueue


def get_queue_data(name):
    q_obj = RedisQueue(name)
    q_re = q_obj.get_all()
    return q_re


class QueueManage(object):

    def __init__(self, name):
        self.q_obj = RedisQueue(name)

    def get_queue_data(self):
        q_re = self.q_obj.get_all()
        return q_re

    def queue_size(self):
        return self.q_obj.qsize()