from django.db import models


class FatSecretEntry(models.Model):
    """Client's data for FatSecret entry."""

    client = models.OneToOneField("users.User", on_delete=models.CASCADE)
    oauth_token = models.CharField(max_length=255, null=True, blank=True)
    oauth_token_secret = models.CharField(
        max_length=255, null=True, blank=True
    )

    def __str__(self):
        return f"Данные доступа клиента: {self.client}"

    class Meta:
        verbose_name = "Данные доступа к Fatsecret"
        verbose_name_plural = "Данные доступа к Fatsecret"
