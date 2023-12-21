from django.contrib import admin

from client.models import Contacts, Health, Log, Note

admin.site.register(Health)
admin.site.register(Contacts)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("__str__", "client", "modelname", "action_time")
    display = ("client", "modelname", "change_message", "action_time")
    readonly_fields = ("action_time",)
    list_filter = ("modelname",)
    search_fields = ("modelname", "change_message")


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("__str__", "client")
    list_filter = ("client",)
