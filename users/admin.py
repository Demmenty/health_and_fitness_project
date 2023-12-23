from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import User

admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "__str__",
        "first_name",
        "last_name",
        "email",
        "is_expert",
        "is_active",
        "is_superuser",
    )
    list_filter = ("is_superuser", "is_active", "is_expert", "sex")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Персональная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "sex",
                    "birthday",
                    "height",
                    "avatar",
                )
            },
        ),
        (
            "Права",
            {
                "fields": (
                    "is_expert",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
