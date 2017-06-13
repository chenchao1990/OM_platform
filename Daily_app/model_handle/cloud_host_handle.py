#!/usr/bin/env python
# _*_coding:utf-8 _*_

from Daily_app.models import cloud_hosts_models


def get_all_data():
    '''
    获取所有的数据
    '''
    id_list = []
    all_company_data = []
    all_company = cloud_hosts_models.CompanyInfo.objects.all()
    for i in all_company:
        id_list.append((i.id, i.company_name, i.alias_name))            # 取出公司的名称 别名 id
    value_list = ['host_counts', 'add_year', 'add_month', 'add_week']
    for company_tuple in id_list:
        company_dict = {'company_name': company_tuple[1], 'company_alias': company_tuple[2]}
        company_data = cloud_hosts_models.CloudHostCounts.objects.filter(company_id=company_tuple[0]).order_by('add_time').values(*value_list)
        company_dict['company_data'] = list(company_data)
        all_company_data.append(company_dict)
    return all_company_data


def get_all_company():
    '''
    获取所有的公司名称
    '''
    value_list = ['id', 'company_name']
    ret = cloud_hosts_models.CompanyInfo.objects.all().values(*value_list)
    return ret


def add_new_cloud_data(data_list):
    '''
    向主机数据表添加新的数据
    '''
    for data_dict in data_list:

        cloud_hosts_models.CloudHostCounts.objects.create(**data_dict)



