from django.contrib import admin
from .models import Measurement, Questionary, FatSecretEntry, Anthropometry, MeasureColor, MeasureIndex, MeasureColorField, UserSettings

# Register your models here.
admin.site.register(Measurement)
admin.site.register(Questionary)
admin.site.register(FatSecretEntry)
admin.site.register(Anthropometry)
admin.site.register(UserSettings)
admin.site.register(MeasureColor)
admin.site.register(MeasureIndex)
admin.site.register(MeasureColorField)