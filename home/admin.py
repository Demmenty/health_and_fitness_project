from django.contrib import admin

from home.models import ConsultRequest


@admin.register(ConsultRequest)
class ConsultRequestAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "age",
        "location",
        "email",
        "contacts",
        "date",
        "is_read",
        "comment",
    )
    readonly_fields = ("date",)
    list_display = ("__str__", "name", "date", "is_read")
    list_filter = ("name", "is_read")
