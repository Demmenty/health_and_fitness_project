from django.contrib.auth.models import User
from django.db import models


class ChatMessage(models.Model):
    """Модель для личного сообщения в чате"""

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="chat/image", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["created_at"]
