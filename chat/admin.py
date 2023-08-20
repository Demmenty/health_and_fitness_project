from django.contrib import admin

from chat.models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "created_at")
    fields = ("sender", "receiver", "text", "image", "created_at", "is_read")
    readonly_fields = ("sender", "receiver", "created_at", "is_read")
