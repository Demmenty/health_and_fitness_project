from django.contrib import admin

from expert.models import ClientMainNote, ClientMonthlyNote


@admin.register(ClientMainNote)
class ClientMainNoteAdmin(admin.ModelAdmin):
    list_display = ("__str__", "client")
    list_filter = ("client",)


@admin.register(ClientMonthlyNote)
class ClientMonthlyNoteAdmin(admin.ModelAdmin):
    list_display = ("__str__", "client", "month", "year")
    list_filter = ("client", "month", "year")
