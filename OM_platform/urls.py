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
from django.conf.urls import url, include
from django.contrib import admin
from Daily_app.views.account import SSOView

urlpatterns = [
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/path/to/media'}),
    url(r'^admin/', admin.site.urls),
    url(r'^sso.html', SSOView.as_view()),
    url(r'^', include('Daily_app.urls')),
    url(r'^', include('ansible_app.urls')),
    url(r'^', include('Budget_app.urls')),
    url(r'^', include('IDC_app.urls')),
]
