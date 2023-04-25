from django.contrib import admin

from .models import MeasureColor, MeasureColorField, MeasureIndex, Measurement

admin.site.register(Measurement)
admin.site.register(MeasureColor)
admin.site.register(MeasureIndex)
admin.site.register(MeasureColorField)
