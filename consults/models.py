from django.db import models


class Request(models.Model):
    """Model for consultation requests from new users"""

    name = models.CharField("Имя", max_length=100, help_text="Как к вам обращаться?")
    age = models.CharField(
        "Возраст", max_length=100, blank=True, help_text="Сколько вам лет?"
    )
    location = models.CharField(
        "Место жительства",
        max_length=100,
        blank=True,
        help_text="Расскажите, откуда вы?",
    )
    email = models.EmailField(
        "Почта",
        max_length=100,
        blank=True,
        help_text="Обещаем не использовать адрес в коварных целях!",
    )
    contacts = models.CharField(
        "Контакты",
        max_length=255,
        help_text="Оставьте ссылку на предпочитаемый способ связи",
    )
    seen = models.BooleanField("Заявка прочитана", default=False)
    comment = models.TextField("Заметка эксперта", default="", blank=True)
    created_at = models.DateField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Заявка № {self.id}"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
