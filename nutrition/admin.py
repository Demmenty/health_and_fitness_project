from django.contrib import admin

from nutrition.models import Estimation, FatSecretEntry

admin.site.register(FatSecretEntry)
admin.site.register(Estimation)
