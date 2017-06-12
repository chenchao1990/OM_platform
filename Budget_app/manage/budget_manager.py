#!/usr/bin/env python
# _*_coding:utf-8 _*_


"""
采购预算的一些处理数据方法归类
"""
from overall.response.base_response import BaseResponse
from overall.response.base_response import BudgetResponse
from Budget_app.model_handle import budget_handle
from Budget_app.execute_excel import read_excel_data
import datetime
import time
import json
import os


def get_budget_data():
    '''
    获取采购的数据
    '''
    response = BudgetResponse()

    try:
        all_department_list = budget_handle.get_all_department_data()                   # 获取所有的部门的名称
        budget_data = budget_handle.get_budget_by_department(all_department_list)       # 根据部门获取所有的采购数据
        all_feild_dict, title_name_list = budget_handle.get_all_verb_name()             # 获取所有字段名 以及中文名,构建head
        response.title_dict = all_feild_dict
        response.title_name = title_name_list
        response.budget_data = budget_data
        response.status = True
        return response
    except Exception, e:
        print e
        response.message = str(e)
        return response


def read_data_from_excel(file_name):
    '''
    从excel表格中读取数据
    '''
    response = BaseResponse()
    from OM_platform.settings import BUDGET_FILE_DIR
    try:
        all_file_list = os.listdir(BUDGET_FILE_DIR)
        for i in all_file_list:
            print "--------------", i
        print "==============", file_name
        data_list = read_excel_data.read_excel_data(BUDGET_FILE_DIR + file_name)
        response.data = data_list
        response.status = True
        return response
    except Exception, e:
        print "eeeeeeeeeeeeeeeeeeeeeeeeeeee", e
        response.message = str(e)
        return response


def delete_data_excel(data):
    '''
    删除excel中所选的行数据
    '''
    response = BaseResponse()
    from OM_platform.settings import BUDGET_FILE_DIR
    try:
        delete_list = json.loads(data.get('delete_list'))
        current_file = data.get("current_file")
        s = read_excel_data.delete_excel_data(BUDGET_FILE_DIR + current_file, delete_list)
        response.data = "OKOKOKOKKK"
        response.status = True
        return response
    except Exception, e:
        print "eeeeeeeeeeeeeeeeeeeeeeeeeeee", e
        response.message = str(e)
        return response


def save_change_data(data):
    '''
    保存表格变更的数据
    '''
    response = BaseResponse()
    from OM_platform.settings import BUDGET_FILE_DIR
    try:
        current_file = data.get('current_file')
        change_dict = json.loads(data.get('update_data'))
        print "current_file", current_file
        s = read_excel_data.save_change_excel(BUDGET_FILE_DIR + current_file, change_dict)
        response.data = "修改成功！！！"
        response.status = True
        return response
    except Exception, e:
        print "eeeeeeeeeeeeeeeeeeeeeeeeeeee", e
        response.message = str(e)
        return response


def add_new_excel_col(data):
    '''
    新增一列表格数据
    '''
    response = BaseResponse()
    from OM_platform.settings import BUDGET_FILE_DIR
    try:
        add_col_list = json.loads(data.get("new_vol"))
        current_file = data.get("current_file")
        if add_col_list:
            read_excel_data.add_new_col(BUDGET_FILE_DIR + current_file, add_col_list)
        else:
            print "no________add_____col____data"
            read_excel_data.add_new_col_end(BUDGET_FILE_DIR + current_file)
        response.data = "增加列成功！"
        response.status = True
        return response
    except Exception, e:
        print "eeeeeeeeeeeeeeeeeeeeeeeeeeee", e
        response.message = str(e)
        return response


def add_new_excel_row(data):
    '''
    新增一行表格数据
    '''
    response = BaseResponse()
    from OM_platform.settings import BUDGET_FILE_DIR
    try:
        add_raw = data.get("action")
        current_file = data.get("current_file")
        print "dddddddddddddddddd2222222222222", add_raw, current_file
        s = read_excel_data.add_new_raw(BUDGET_FILE_DIR + current_file)
        response.data = "增加行成功！"
        response.status = True
        return response
    except Exception, e:
        print "eeeeeeeeeeeeeeeeeeeeeeeeeeee", e
        response.message = str(e)
        return response


def upload_budget_file(file_obj, file_dir):
    '''
    上传表格文件
    '''
    response = BaseResponse()
    try:
        # 保存上传的脚本
        filename = file_obj.name

        file_path = file_dir + filename
        print "upload_file_path", file_path
        f = open(file_path, 'wb')
        for line in file_obj.chunks():              # 保存文件
            f.write(line)
        f.close()

        response.status = True
        response.message = u'上传成功'
        return response
    except AttributeError:
        response.message = u'选择上传文件'
        return response
    except Exception, e:
        print "up____error", str(e)
        response.message = str(e)
        return response


def get_upload_files(file_dir):
    '''
    获取budget目录下所有的文件
    '''
    Kilobyte = 1000
    Megabyte = float(1000*Kilobyte)
    Gigabyte = float(1000*Megabyte)

    response = BaseResponse()
    try:
        file_list = []
        all_file_list = os.listdir(file_dir)
        for file_name in all_file_list:
            t_dict = {}
            # dt = datetime.datetime.strptime(pageTime, "%Y-%m-%d %H:%M:%S")
            file_path = os.path.join(file_dir, file_name.decode('utf8'))
            file_obj = os.stat(file_path)
            str_t = file_obj.st_ctime
            f_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(str_t))  # 文件修改时间
            change_time = datetime.datetime.strptime(f_time, "%Y-%m-%d %H:%M:%S")
            d = change_time + datetime.timedelta(hours=8)
            nTime = d.strftime("%Y-%m-%d %H:%M:%S")
            f_size = float(file_obj.st_size)
            if f_size < 1000000:
                f_size = str(f_size / Kilobyte) + 'KB'
            else:
                f_size = str(f_size/Megabyte) + 'MB'
            t_dict['filename'] = file_name.decode('utf8')
            t_dict['filesize'] = f_size
            t_dict['filetime'] = nTime
            file_list.append(t_dict)
        response.data = file_list
        response.status = True
        return response

    except Exception, e:
        response.message = str(e)
        return response


def delete_upload_file(filename, file_dir):
    '''
    删除用户所选的文件
    '''
    response = BaseResponse()
    try:
        file_path = file_dir + filename
        if os.path.isfile(file_path):
            os.remove(file_path)
            response.status = True
            return response
        else:
            response.message = u'删除失败'
            return response
    except Exception, e:
        response.message = str(e)
        return response




