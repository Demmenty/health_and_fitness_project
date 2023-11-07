from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("register-client", views.register_client, name="register_client"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path(
        "password-reset/", views.PasswordReset.as_view(), name="password_reset"
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        views.PasswordResetConfirm.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/done/",
        views.PasswordResetDone.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset-complete/",
        views.PasswordResetComplete.as_view(),
        name="password_reset_complete",
    ),
    path(
        "password-reset-email/",
        views.PasswordReset.as_view(),
        name="password-reset-email",
    ),
    path(
        "password-change/",
        views.PasswordChange.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        views.PasswordChangeDone.as_view(),
        name="password_change_done",
    ),
]
