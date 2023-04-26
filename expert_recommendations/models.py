from django.contrib.auth.models import User
from django.db import models


class NutritionRecommendation(models.Model):
    """модель для хранения рекомендуемых уровней потребления
    КБЖУ для клиента от эксперта"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calories = models.PositiveSmallIntegerField(
        "Рекомендуемое количество калорий", null=True, blank=True
    )
    protein = models.PositiveSmallIntegerField(
        "Рекомендуемое количество белков", null=True, blank=True
    )
    fats = models.PositiveSmallIntegerField(
        "Рекомендуемое количество жиров", null=True, blank=True
    )
    carbohydrates = models.PositiveSmallIntegerField(
        "Рекомендуемое количество углеводов", null=True, blank=True
    )
    note = models.TextField("Заметка", default="", blank=True)

    def __str__(self):
        return f"Рекомендуемый уровень КБЖУ для клиента {self.user}"
    
    class Meta:
        verbose_name = "Рекомендация КБЖУ"
        verbose_name_plural = "Рекомендации КБЖУ"
