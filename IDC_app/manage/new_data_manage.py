#!/usr/bin/env python
# _*_coding:utf-8 _*_
from overall.response.base_response import BaseResponse
from IDC_app.models import IDCPhysical
import json
import re
import xlrd


def read_excel_data():
    '''
    读取excel文件中的数据
    '''
    excel_path = "test.xlsx"
    file_obj = xlrd.open_workbook(excel_path)
    sheet0_obj = file_obj.sheet_by_index(0)

    all_rows = sheet0_obj.nrows         # 获取表格中行总数
    data_list = []
    for line_num in range(1, all_rows):
        row_data_list = sheet0_obj.row_values(line_num)
        data_list.append(row_data_list)
    return data_list


def create_new_data():
    # 读取excel文件
    # 将表格中的数据一一对应，生成数据列表
    # 写入数据库
    response = BaseResponse()
    try:
        import_data_list = []
        all_data_list = read_excel_data()
        for line in all_data_list:
            if type(line[18]) == float:

                line[18] = int(line[18])
            one_obj = IDCPhysical(pro_type=line[0],
                                  ip=line[1],
                                  device_type=line[2],
                                  server_type=line[3],
                                  app_type=line[4],
                                  device_status=line[5],
                                  is_virtual=line[6],
                                  sn=line[7],
                                  brand=line[8],
                                  device_version=line[9],
                                  device_conf=line[10],
                                  own_person=line[11],
                                  pro_line1=line[12],
                                  pro_line2=line[13],
                                  pro_line3=line[14],
                                  pro_person=line[15],
                                  module=line[16],
                                  idc=line[17],
                                  cabinet=line[18],
                                  cabinet_status=line[19],
                                  time_period=line[20],
                                  delivery_date=line[21])
            import_data_list.append(one_obj)
        IDCPhysical.objects.bulk_create(import_data_list)
        response.status = True
        response.data = "import data successfule...."

    except Exception, e:
        print "eeeeeeeeeeeeeeeeeeerror", e
        response.message = str(e)
    return response
