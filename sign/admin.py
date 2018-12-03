from django.contrib import admin
from sign.models import Event, Guest


# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "status", "address", "start_time"]
    search_fields = ["name", "phone"]
    list_filter = ["status"]


class GuestAdmin(admin.ModelAdmin):
    list_display = ["realname", "phone", "email", "sign", "create_time", "event"]

admin.site.register(Event, EventAdmin)
admin.site.register(Guest,GuestAdmin)   # 这些代码让admin管理工具为这些模块提供页面

