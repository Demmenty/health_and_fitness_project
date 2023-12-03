from django.db import models


class FatSecretEntry(models.Model):
    """Client's data for FatSecret entry."""

    client = models.OneToOneField("users.User", on_delete=models.CASCADE)
    oauth_token = models.CharField(max_length=255, null=True, blank=True)
    oauth_token_secret = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Доступ к Fatsecret: {self.client}"

    class Meta:
        verbose_name = "Данные доступа к Fatsecret"
        verbose_name_plural = "Данные доступа к Fatsecret"


class Recommendation(models.Model):
    """Nutrition recommendations for the client."""

    client = models.OneToOneField("users.User", on_delete=models.CASCADE)
    calories = models.PositiveSmallIntegerField("Калории", null=True, blank=True)
    protein = models.PositiveSmallIntegerField("Белки", null=True, blank=True)
    fat = models.PositiveSmallIntegerField("Жиры", null=True, blank=True)
    carbohydrate = models.PositiveSmallIntegerField("Углеводы", null=True, blank=True)
    comment = models.TextField("Комментарий", default="", blank=True)

    def __str__(self):
        return f"Рекомендации КБЖУ: {self.client}"

    class Meta:
        verbose_name = "Рекомендации КБЖУ"
        verbose_name_plural = "Рекомендации КБЖУ"
