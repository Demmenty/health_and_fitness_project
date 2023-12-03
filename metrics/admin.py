from django.contrib import admin

from metrics.models import (
    Anthropometry,
    AnthropometryPhotoAccess,
    Colors,
    DailyData,
    Levels,
)


@admin.register(DailyData)
class DailyDataAdmin(admin.ModelAdmin):
    ordering = ("-date",)
    list_display = (
        "__str__",
        "client",
        "feel",
        "date",
    )
    list_filter = ("client",)


@admin.register(Levels)
class LevelsAdmin(admin.ModelAdmin):
    ordering = ("client", "parameter")
    list_display = (
        "__str__",
        "client",
        "parameter",
    )
    list_filter = ("client", "parameter")


admin.site.register(Colors)
admin.site.register(Anthropometry)
admin.site.register(AnthropometryPhotoAccess)
