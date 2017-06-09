from django.contrib import admin

# Register your models here.

from Budget_app import models


class PurchaseBudget(admin.ModelAdmin):
    list_display = ("project_name", "duty_person", "device_model", "plan_phy_quantity")
admin.site.register(models.PurchaseBudget, PurchaseBudget)


class Department(admin.ModelAdmin):
    list_display = ("name", "cn_name")
admin.site.register(models.Department, Department)



