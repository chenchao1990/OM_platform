#!/usr/bin/env python
# _*_coding:utf-8 _*_

import xlrd
import xlwt
from xlutils.copy import copy


def read_excel_data(excel_path):
    '''
    读取excel文件中的数据
    '''
    file_obj = xlrd.open_workbook(excel_path)
    sheet0_obj = file_obj.sheet_by_index(0)

    all_rows = sheet0_obj.nrows         # 获取表格中行总数
    data_list = []
    for line_num in range(all_rows):
        row_data_list = sheet0_obj.row_values(line_num)
        data_list.append(row_data_list)

    return data_list


def delete_excel_data(excel_path, delete_list):
    '''
    删除excel文件中的数据
    '''
    old_workbook = xlrd.open_workbook(excel_path)
    new_excel = xlwt.Workbook()                 # 用于写入数据的新excel
    new_sheet = new_excel.add_sheet(u'sheet1')

    sheet1 = old_workbook.sheet_by_index(0)             # 获取第一个sheet
    rows_num = sheet1.nrows                         # 表格中所有的行数
    new_data_list = []              # 将新数据保存到此

    for i in range(rows_num):
        if str(i) not in delete_list:
            current_row_list = sheet1.row_values(i)
            new_data_list.append(current_row_list)

    for y, value_list in enumerate(new_data_list):
        for x, value in enumerate(value_list):
            new_sheet.write(y, x, value)

    new_excel.save(excel_path)
    return True


def save_change_excel(excel_path, change_dict):
    '''
    更新表格中 变更的数据
    '''
    workbook = xlrd.open_workbook(excel_path)         # 读取带格式的表格
    # sheet1 = workbook.sheet_by_index(0)             # 获取第一个sheet
    new_excel = copy(workbook)
    new_sheet = new_excel.get_sheet(0)
    for x_y, value in change_dict.items():
        position_list = x_y.split('-')
        x = int(position_list[0])
        y = int(position_list[1])

        new_sheet.write(y, x, value)
    new_excel.save(excel_path)
    return True


def add_new_col(excel_path, add_col_list):
    '''
    更新表格中 变更的数据
    '''
    new_excel = xlwt.Workbook()                 # 用于写入数据的新excel
    new_sheet = new_excel.add_sheet(u'sheet1')

    workbook = xlrd.open_workbook(excel_path)         # 读取带格式的表格
    old_sheet = workbook.sheet_by_index(0)
    all_rows = old_sheet.nrows         # 所有的行数
    all_len = len(add_col_list)         # 获取增加的列数
    for y in range(all_rows):
        current_row_list = old_sheet.row_values(y)    # 循环的当前行数据列表
        if y == 0:
            for n in range(all_len):
                all_col_dict = add_col_list[n]
                x = int(all_col_dict['x_num'])
                value = all_col_dict['input_val']
                current_row_list.insert(x+n, value)
        else:
            for n in range(all_len):
                all_col_dict = add_col_list[n]
                x = int(all_col_dict['x_num'])
                value = ""
                current_row_list.insert(x+n, value)
        for x, val in enumerate(current_row_list):
            new_sheet.write(y, x, val)
    new_excel.save(excel_path)
    return True












