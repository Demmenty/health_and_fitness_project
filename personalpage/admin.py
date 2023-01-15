from django.contrib import admin
from .models import Questionary, Anthropometry, UserSettings


admin.site.register(Questionary)
admin.site.register(Anthropometry)
admin.site.register(UserSettings)
