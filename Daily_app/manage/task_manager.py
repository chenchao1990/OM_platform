#!/usr/bin/env python
# _*_coding:utf-8 _*_

from Daily_app.models import user_models
from Daily_app.models import task_models
from overall.response.base_response import TaskResponse
from Daily_app.model_handle import task_handle, user_handle
import datetime
import calendar


def current_time():
    w = datetime.datetime.now()
    s = str(w).split(".")[0]
    return s


def get_task(month_num, current_day=None):
    '''
    获取一个月的值班数据
    '''
    response = TaskResponse()
    try:
        if current_day:
            if current_day < 10:
                current_day = "0" + str(current_day)
            response.current_day = current_day              # 当月当天的数字
        ret = task_handle.get_task_by_month(month_num)      # 获取某个月份的数据
        response.status = 1
        response.data = list(ret)
        response.current_time = current_time()          # 获取当前时间
        response.current_month = current_month(month_num-1)
    except Exception, e:
        response.message = str(e)
    return response


def create_task_data(year_num):
    '''
    1、将DBA用户和SA用户 电话获取到
    2、生成日期和星期
    3、写入数据
    '''
    dba_list = []
    sa_list = []
    dba_obj_list = user_handle.get_dba_user()
    sa_obj_list = user_handle.get_sa_user()
    for dba in dba_obj_list:
        name = dba.name                     # 获取用户名
        tel = dba.mobile                    # 获取电话
        task_id = dba.task_id               # 获取值班序列
        dba_list.append({"name": name, "tel": tel, "task_id": task_id})
    for sa in sa_obj_list:
        name = sa.cn_name                     # 获取用户名
        tel = sa.mobile                    # 获取电话
        print "sa................tel", tel
        task_id = sa.task_id               # 获取值班序列
        sa_list.append({"name": name, "tel": tel, "task_id": task_id})

    dba_id_list = []
    for i in dba_list:
        dba_id_list.append(i['task_id'])

    sa_id_list = []
    for i in sa_list:
        sa_id_list.append(i['task_id'])

    db_sortd_list = sorted(dba_id_list)
    sa_sortd_list = sorted(sa_id_list)

    re_db_list = []                 # 排序之后的数据列表
    re_sa_list = []
    for num in db_sortd_list:     # 循环排序之后的dba id list

        for value in dba_list:      # 循环存放数据的dba list
            task_id = value["task_id"]
            if task_id == num:
                re_db_list.append(value)

    for num in sa_sortd_list:     # 循环排序之后的dba id list

        for value in sa_list:      # 循环存放数据的dba list
            task_id = value["task_id"]
            if task_id == num:
                re_sa_list.append(value)

    # mon_list = [1, 2]         # 一共12个月
    mon_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]         # 一共12个月
    d_list = []

    len_dba = len(dba_list) - 1
    len_sa = len(sa_list) - 1
    dba_num = 0
    sa_num = 0

    for mon_num in mon_list:

        mon_days = calendar.monthrange(2017, mon_num)[1]            # 每个月天数

        for i in range(1, mon_days+1):

            office_place = ''
            s = datetime.datetime(2017, mon_num, i)
            week = change_week(s.weekday())                 # 星期几
            if s.weekday() == 5 or s.weekday() == 6:
                office_place = u'远程'
            d = str(s).split(' ')[0]                        # 日期
            c_day = str(s).split(' ')[0].split('-')[2].strip()        # 当天号数

            # db_user = re_db_list[dba_num]['name']           # DBuser
            # db_tel = re_db_list[dba_num]['tel']             # DB tel

            sa_user = re_sa_list[sa_num]['name']             # sa tel
            sa_tel = re_sa_list[sa_num]['tel']                  # sa tel

            value_dict = {"date_str": d,
                          "week_str": week,
                          # "dba_user": db_user, "dba_tel": db_tel,
                          "sa_user": sa_user, "sa_tel":sa_tel,
                          "month_num": mon_num,
                          "day_num": c_day,
                          'office_place': office_place}
            task_handle.create_task_data(value_dict)
            dba_num += 1
            sa_num += 1
            if dba_num > len_dba:
                dba_num = 0
            if sa_num > len_sa:
                sa_num = 0


def change_week(num):
    '''
    将数字转换为星期
    '''
    s = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return s[num]


def current_month(num):
    '''
    将数字转换为星期
    '''
    n = ['一月', '二月', '三月', '四月', '五月', '六月', '七月' , '八月', '九月', '十月', '十一月', '十二月']
    return n[num]


