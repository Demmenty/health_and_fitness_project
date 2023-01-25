from django.contrib import admin
from .models import Commentary, Clientnote, FullClientnote


admin.site.register(Commentary)
admin.site.register(Clientnote)
admin.site.register(FullClientnote)
