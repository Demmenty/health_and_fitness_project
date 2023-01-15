from django.contrib import admin
from .models import Measurement, MeasureColor, MeasureIndex, MeasureColorField


admin.site.register(Measurement)
admin.site.register(MeasureColor)
admin.site.register(MeasureIndex)
admin.site.register(MeasureColorField)