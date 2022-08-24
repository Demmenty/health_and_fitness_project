from django.contrib import admin
from .models import Measurement, Questionary, FatSecretEntry

# Register your models here.
admin.site.register(Measurement)
admin.site.register(Questionary)
admin.site.register(FatSecretEntry)