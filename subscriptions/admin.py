from django.contrib import admin

from subscriptions.models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "access",
        "coaching",
        "default_price",
    )
    list_filter = ("access", "coaching")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "client",
        "plan",
        "start_date",
        "end_date",
    )
    list_filter = ("client", "plan")
