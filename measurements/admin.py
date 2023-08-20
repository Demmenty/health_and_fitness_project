from django.contrib import admin

from measurements.models import (
    Anthropometry,
    AnthropometryPhotoAccess,
    MeasureColor,
    MeasureColorField,
    MeasureIndex,
    Measurement,
)

admin.site.register(Measurement)
admin.site.register(MeasureColor)
admin.site.register(MeasureIndex)
admin.site.register(MeasureColorField)
admin.site.register(Anthropometry)
admin.site.register(AnthropometryPhotoAccess)
