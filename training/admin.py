from django.contrib import admin

from .models import Exercise, ExerciseReport, Training

admin.site.register(Exercise)
admin.site.register(Training)
admin.site.register(ExerciseReport)
