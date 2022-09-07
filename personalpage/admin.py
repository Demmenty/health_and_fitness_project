from django.contrib import admin
from .models import Measurement, Questionary, FatSecretEntry, Anthropometry

# Register your models here.
admin.site.register(Measurement)
admin.site.register(Questionary)
admin.site.register(FatSecretEntry)
admin.site.register(Anthropometry)