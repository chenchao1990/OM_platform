"""OM_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Daily_app.views import iptables
from Daily_app.views import account
from Daily_app.views import log
from Daily_app.views import task
from Daily_app.views import connection
from Daily_app.views import password_
from Daily_app.views import smtp_
urlpatterns = [

    url(r'account/login/', account.login),
    url(r'account/logout/', account.logout_sso),

    url(r'test/', iptables.test),
    url(r'^$', iptables.index),
    url(r'iptables/init/$', iptables.iptables_init),
    url(r'iptables/init_rules/$', iptables.iptables_rules),
    url(r'iptables/init_execute/$', iptables.iptables_init_execute),
    url(r'iptables/check/$', iptables.iptables_check),
    url(r'iptables/check_rules/$', iptables.iptables_rules_check),
    url(r'iptables/add/$', iptables.iptables_rules_add),

    url(r'iptables/add/quick/$', iptables.iptables_add_quick),
    url(r'iptables/add/cmd/$', iptables.iptables_add_cmd),

    url(r'log/iptables/$', log.iptables_log),
    url(r'log/iptables_show/$', log.iptables_log_show),
    url(r'log/password/$', log.password_log),
    url(r'log/password_log_show/$', log.password_log_show),

    url(r'task/$', task.task_show),
    url(r'task_auth/$', task.task_show_auth),
    url(r'task/show_all/$', task.task_show_all),
    url(r'task/show_month/$', task.task_show_month),
    url(r'task/create/$', task.create_task_data),

    url(r'connection/ping/$', connection.ping),
    url(r'connection/single_ping/$', connection.single_ping),
    url(r'connection/rang_ping/$', connection.rang_ping),
    url(r'connection/file_ping/$', connection.file_ping),
    url(r'connection/upload_ping_file/$', connection.upload_ping_file),
    url(r'connection/get_ping_file/$', connection.get_ping_file),
    url(r'connection/delete_ping_file/$', connection.delete_ping_file),

    # url(r'password/$', password_.password_init),
    url(r'password/check/$', password_.password_check),
    url(r'password/upload_pwd_file/$', password_.upload_password_file),
    url(r'password/get_pwd_file/$', password_.get_password_file),
    url(r'password/delete_pwd_file/$', password_.delete_password_file),
    url(r'password/run_check_file/$', password_.run_check_file),

    url(r'password/import/$', password_.password_import),
    url(r'password/init/$', password_.password_init),
    url(r'password/get_queue/$', password_.password_queue_data),

    url(r'password/server/$', password_.password_server),
    url(r'password/upload_server_file/$', password_.upload_password_server),
    url(r'password/get_server_file/$', password_.get_server_file),
    url(r'password/delete_server_file/$', password_.delete_server_file),
    url(r'password/change_server_pwd/$', password_.change_server_pwd),

    url(r'smtp/$', smtp_.smtp_),
    url(r'smtp/add/$', smtp_.smtp_add),


    url(r'iptables_api/$', iptables.iptables_api),


    url(r'cloud/$', task.cloud_host),
    url(r'cloud/show_data/$', task.get_host_data),
    url(r'cloud/new_data/$', task.cloud_host),
    url(r'cloud/new_company/$', task.add_new_company),
    url(r'cloud/delete_data/$', task.delete_day_data),



]
