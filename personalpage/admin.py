from django.contrib import admin
from .models import Measurement, Questionary

# Register your models here.
admin.site.register(Measurement)
admin.site.register(Questionary)