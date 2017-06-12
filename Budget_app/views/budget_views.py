#!/usr/bin/env python
# _*_coding:utf-8 _*_
from django.shortcuts import render
from django.shortcuts import HttpResponse
from Daily_app.views.account import login_sso
from Budget_app.manage import budget_manager
from OM_platform import settings
import json


@login_sso
def budget_view(request):
    '''
    预算页面
    '''
    user_info = request.userinfo
    print "------------------------", request.GET.get('name')
    return render(request, 'budget/budget_show.html', {'userinfo': user_info})


@login_sso
def budget_data_get(request):
    '''
    获取采购预算的数据 展示到前端页面
    '''
    if request.method == "POST":
        ret = budget_manager.get_budget_data().__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def budget_data_from_excel(request):
    '''
    获取采购预算的数据 展示到前端页面
    '''
    if request.method == 'POST':
        print "11111111111111"
        file_name = request.POST.get('file_name')
        ret = budget_manager.read_data_from_excel(file_name).__dict__

        return HttpResponse(json.dumps(ret))


@login_sso
def delete_excel_tr(request):
    '''
    删除行数据
    '''
    data = request.POST
    # delete_list = data.get('delete_list')
    # delete_list = json.loads(request.POST.get('delete_list'))
    print "ddddddddddddddddd", data
    ret = budget_manager.delete_data_excel(data).__dict__

    return HttpResponse(json.dumps(ret))


@login_sso
def save_change_data(request):
    '''
    保存更新的数据
    '''
    # data = json.loads(request.POST)
    # delete_list = data.get('delete_list')
    change_data = json.loads(request.POST.get('update_data'))
    data = request.POST
    print "ddddddddddddddddd", change_data
    print "ddddddddddddddddd", request.POST
    ret = budget_manager.save_change_data(data).__dict__

    return HttpResponse(json.dumps(ret))


@login_sso
def add_new_col(request):
    '''
    保存更新的数据
    '''
    # add_col_data = json.loads(request.POST.get('new_vol'))
    data = request.POST
    print "ddddddddddddddddd-------------------------", data
    ret = budget_manager.add_new_excel_col(data).__dict__

    return HttpResponse(json.dumps(ret))


@login_sso
def add_new_row(request):
    '''
    新增一行
    '''

    data = request.POST
    print "ddddddddddddddddd", data
    ret = budget_manager.add_new_excel_row(data).__dict__

    return HttpResponse(json.dumps(ret))


@login_sso
def budget_list(request):
    '''
    预算表格文件管理页面
    '''
    user_info = request.userinfo
    return render(request, 'budget/budget_file_list.html', {'userinfo': user_info})


@login_sso
def upload_budget_file(request):
    '''
    上传表格
    '''
    file_dir = settings.BUDGET_FILE_DIR                    # 导入接受IP文件目录
    if request.method == "POST":
        budget_file = request.FILES
        file_obj = budget_file.get('upload_filename')       # 根据前端设置的name属性值获取相对应的文件
        ret = budget_manager.upload_budget_file(file_obj, file_dir).__dict__
        return HttpResponse(json.dumps(ret))


@login_sso
def show_budget_file(request):
    '''
    获取目录下所有上传的表格文件
    '''
    budget_dir = settings.BUDGET_FILE_DIR
    ret = budget_manager.get_upload_files(budget_dir).__dict__
    return HttpResponse(json.dumps(ret))


@login_sso
def delete_file(request):
    '''
    删除目录中上传的文件
    '''
    if request.method == "POST":
        filename = request.POST.get('filename')

        file_dir = settings.BUDGET_FILE_DIR
        ret = budget_manager.delete_upload_file(filename, file_dir).__dict__
        return HttpResponse(json.dumps(ret))






