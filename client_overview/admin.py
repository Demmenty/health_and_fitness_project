from django.contrib import admin

from client_overview.models import ClientContact, HealthQuestionary, MeetQuestionary


admin.site.register(HealthQuestionary)
admin.site.register(MeetQuestionary)
admin.site.register(ClientContact)
