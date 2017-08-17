# _*_coding:utf-8 _*_
from django.contrib import admin

# Register your models here.

from IDC_app import models

admin.site.register(models.IDCPhysical)
admin.site.register(models.ProjectType)
admin.site.register(models.DeviceType)
admin.site.register(models.ServerType)
admin.site.register(models.AppType)
admin.site.register(models.DeviceStatus)
admin.site.register(models.IsVirtual)
admin.site.register(models.Brand)
admin.site.register(models.DeviceVersion)
admin.site.register(models.Personal)
admin.site.register(models.ProductLine1)
admin.site.register(models.ProductLine2)
admin.site.register(models.ProductLine3)
admin.site.register(models.ProductPerson)
admin.site.register(models.Module)
admin.site.register(models.IDC)
admin.site.register(models.CabinetStatus)


