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
from Budget_app.views import budget_views
urlpatterns = [
    url(r'budget_show/$', budget_views.budget_view),
    url(r'budget_data_get/$', budget_views.budget_data_get),
    url(r'budget_data_excel/$', budget_views.budget_data_from_excel),
    url(r'delete_checked_tr/$', budget_views.delete_excel_tr),
    url(r'updata_data/$', budget_views.save_change_data),
    url(r'add_new_col/$', budget_views.add_new_col),
    url(r'add_new_row/$', budget_views.add_new_row),
    url(r'budget_list/$', budget_views.budget_list),
    url(r'show_all_budget/$', budget_views.show_budget_file),
    url(r'upload_budget_file/$', budget_views.upload_budget_file),
    url(r'delete_excel/$', budget_views.delete_file),


]
