from django.db import models
from PIL import Image

from chat.managers import MessageManager
from users.models import User


class Message(models.Model):
    """Chat message between client and expert"""

    objects = MessageManager()

    sender = models.ForeignKey(
        User,
        verbose_name="Отправитель",
        on_delete=models.CASCADE,
        related_name="sender",
    )
    recipient = models.ForeignKey(
        User,
        verbose_name="Получатель",
        on_delete=models.CASCADE,
        related_name="recipient",
    )

    text = models.TextField("Текст", null=True, blank=True)
    image = models.ImageField(
        "Изображение", upload_to="chat/image", null=True, blank=True
    )
    image_width = models.PositiveSmallIntegerField(
        "Ширина изображения (пиксели)", null=True, blank=True
    )
    image_height = models.PositiveSmallIntegerField(
        "Высота изображения (пиксели)", null=True, blank=True
    )
    audio = models.FileField("Аудио", upload_to="chat/audio", null=True, blank=True)

    seen = models.BooleanField("Прочитано", default=False)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image and not self.image_width and not self.image_height:
            image = Image.open(self.image.path)
            self.image_width, self.image_height = image.size
            self.save()

    def __str__(self):
        return f"Сообщение {self.id}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["created_at"]
