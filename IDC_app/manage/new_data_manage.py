#!/usr/bin/env python
# _*_coding:utf-8 _*_
from overall.response.base_response import BaseResponse
from IDC_app.models import IDCPhysical
import json
import re
import xlrd


def upload_idc_file(file_obj, filename, up_dir):
    '''
    将文件上传至目录下
    '''
    response = BaseResponse()
    try:
        # 保存上传的文件
        if not filename.endswith("xlsx"):
            response.message = u"文件格式错误"
            return response
        file_dir = up_dir + filename
        f = open(file_dir, 'wb')
        for line in file_obj.chunks():              # 保存文件
            f.write(line)
        f.close()
        response.data = file_dir
        response.status = True
        return response

    except Exception, e:
        response.message = str(e)
        return response


def read_excel_data(excel_path):
    '''
    读取excel文件中的数据
    '''
    file_obj = xlrd.open_workbook(str(excel_path))
    sheet0_obj = file_obj.sheet_by_index(0)

    all_rows = sheet0_obj.nrows         # 获取表格中行总数
    data_list = []
    for line_num in range(1, all_rows):
        row_data_list = sheet0_obj.row_values(line_num)
        data_list.append(row_data_list)
    return data_list


def create_new_data(file_obj, file_path, filename):
    # 读取excel文件
    # 将表格中的数据一一对应，生成数据列表
    # 写入数据库
    response = BaseResponse()
    try:
        import_data_list = []

        new_file_obj = upload_idc_file(file_obj, filename, file_path)
        if not new_file_obj.status:
            response.message = new_file_obj.message
            return response
        all_data_list = read_excel_data(new_file_obj.data)
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
        response.data = "success"

    except Exception, e:
        print "eeeeeeeeeeeeeeeeeeerror", e
        response.message = str(e)
    return response
