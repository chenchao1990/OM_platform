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
from IDC_app.views import new_data
from IDC_app.views import collect_data
urlpatterns = [

    url(r'idc/$', new_data.idc_list),
    url(r'idc/check_data/$', new_data.check_data),
    url(r'idc/data_update/$', new_data.update_data),
    url(r'idc/idc_file/up/$', new_data.add_new_data),
    # url(r'idc/data/create/$', new_data.add_new_data),
    url(r'idc/statistics/$', collect_data.statistics),


]


