from django.contrib import admin

from chat.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "sender", "recipient", "created_at")
    list_filter = ("sender", "recipient")
    ordering = ("-created_at",)
