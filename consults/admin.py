from django.contrib import admin

from consults.models import Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    fields = (
        "created_at",
        "name",
        "age",
        "location",
        "email",
        "contacts",
        "seen",
        "comment",
    )
    readonly_fields = ("created_at",)
    list_display = ("__str__", "name", "created_at", "seen")
    list_filter = ("name", "seen")
