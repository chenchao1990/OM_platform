from django.contrib import admin

# Register your models here.

from Daily_app.models import iptables_models
from Daily_app.models import user_models
from Daily_app.models import task_models
from Daily_app.models import cloud_hosts_models

admin.site.register(iptables_models.IptablesInit)
admin.site.register(iptables_models.IptablesBelong)
admin.site.register(iptables_models.IptablesQuick)
admin.site.register(iptables_models.LogType)


class IptablesLog(admin.ModelAdmin):
    list_display = ("log_type", "login_user", "msg")
admin.site.register(iptables_models.IptablesLog, IptablesLog)


class UserInfo(admin.ModelAdmin):
    list_display = ("cn_name", "task_id", "email", "user_auth")
admin.site.register(user_models.UserInfo, UserInfo)


class AdminInfo(admin.ModelAdmin):
    list_display = ("username",)
admin.site.register(user_models.AdminInfo, AdminInfo)


class UserType(admin.ModelAdmin):
    list_display = ("caption", "code")
admin.site.register(user_models.UserType, UserType)


class Task(admin.ModelAdmin):
    list_display = ("date_str", "week_str", "dba_user", "sa_user")
admin.site.register(task_models.TaskData, Task)


class Company(admin.ModelAdmin):
    list_display = ("company_name", "alias_name")
admin.site.register(cloud_hosts_models.CompanyInfo, Company)


class CloudHostCounts(admin.ModelAdmin):
    list_display = ("company_id", "add_year", "add_month", "add_week", "host_counts")
admin.site.register(cloud_hosts_models.CloudHostCounts, CloudHostCounts)


class IptablesUser(admin.ModelAdmin):
    list_display = ("user", "ip", "p_key")
admin.site.register(user_models.IptablesAuth, IptablesUser)



















