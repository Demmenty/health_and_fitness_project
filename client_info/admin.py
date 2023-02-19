from django.contrib import admin
from .models import HealthQuestionary, MeetQuestionary, ClientContact


admin.site.register(HealthQuestionary)
admin.site.register(MeetQuestionary)
admin.site.register(ClientContact)
