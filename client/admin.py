from django.contrib import admin

from client.models import Contacts, Health, Log, MainData

admin.site.register(Health)
admin.site.register(Contacts)


@admin.register(MainData)
class MainDataAdmin(admin.ModelAdmin):
    list_display = ("__str__", "client", "sex", "birthday")
    display = ("client", "sex", "height", "birthday", "avatar")
    readonly_fields = ("sex", "birthday")
    list_filter = ("sex",)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("__str__", "client", "modelname", "action_time")
    display = ("client", "modelname", "change_message", "action_time")
    readonly_fields = ("action_time",)
    list_filter = ("modelname",)
    search_fields = ("modelname", "change_message")
