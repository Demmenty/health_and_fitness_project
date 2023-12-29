from django.contrib.auth.models import User
from django.db import models


class FatSecretEntry(models.Model):
    """Модель для хранения данных входа в FatSecret"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    oauth_token = models.CharField(max_length=255, null=True, blank=True)
    oauth_token_secret = models.CharField(
        max_length=255, null=True, blank=True
    )

    def __str__(self):
        return f"Данные для использования FS клиента {self.user}"

    class Meta:
        verbose_name = "Данные для входа в Fatsecret"
        verbose_name_plural = "Данные для входа в Fatsecret"
