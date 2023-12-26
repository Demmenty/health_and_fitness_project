from django.contrib import admin

from client.models import Contacts, Food, Goal, Health, Log, Note, Sleep, Weight


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("__str__", "client", "modelname", "action_time")
    display = ("client", "modelname", "change_message", "action_time")
    readonly_fields = ("action_time",)
    list_filter = ("modelname",)
    search_fields = ("modelname", "change_message")


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("__str__", "client")
    list_filter = ("client",)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("__str__", "client")
    list_filter = ("client",)


@admin.register(Health)
class HealthAdmin(admin.ModelAdmin):
    list_display = ("__str__", "client")
    list_filter = ("client",)


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ("__str__", "client")
    list_filter = ("client",)


@admin.register(Sleep)
class SleepAdmin(admin.ModelAdmin):
    list_display = ("__str__", "client")
    list_filter = ("client",)


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ("__str__", "client")
    list_filter = ("client",)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("__str__", "client")
    list_filter = ("client",)
