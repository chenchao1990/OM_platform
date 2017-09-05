#!/usr/bin/env python
# _*_coding:utf-8 _*_

from Daily_app.models.task_models import TaskData


def get_task_by_month(num):
    ret = TaskData.objects.filter(month_num=num).order_by('id').values()
    return ret


def get_task_all():
    ret = TaskData.objects.all().order_by('id').values()
    return ret


def create_task_data(value_dict):
    TaskData.objects.create(**value_dict)


def delete_all_task():
    TaskData.objects.all().delete()