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
from ansible_app.views import flying_duck
urlpatterns = [
    url(r'^$', iptables.index),

    url(r'ansible/cmd/', flying_duck.cmd_view),
    url(r'ansible/cmd_run/', flying_duck.cmd_execute),
    url(r'ansible/file/', flying_duck.file_view),
    url(r'ansible/upload_file/', flying_duck.upload_file),
    url(r'ansible/upload_ip_file/', flying_duck.upload_ip_file),
    url(r'ansible/get_all_file/', flying_duck.get_all_files),
    url(r'ansible/get_all_script/', flying_duck.get_all_scripts),
    url(r'ansible/dispense_file/', flying_duck.dispense_file),
    url(r'ansible/delete_file/', flying_duck.delete_file),
    url(r'ansible/run_script/', flying_duck.execute_script),
    url(r'ansible/upload_script/', flying_duck.upload_script),
    url(r'ansible/trigger_script/', flying_duck.run_script),

    # url(r'ansible/file/', flying_duck.cmd_execute),



]
