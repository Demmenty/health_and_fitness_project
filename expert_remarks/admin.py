from django.contrib import admin

from .models import Clientnote, Commentary, FullClientnote

admin.site.register(Commentary)
admin.site.register(Clientnote)
admin.site.register(FullClientnote)
