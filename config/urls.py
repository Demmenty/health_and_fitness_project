from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("main.urls", namespace="main")),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("consults/", include("consults.urls", namespace="consults")),
    path("client/", include("client.urls", namespace="client")),
    path("expert/", include("expert.urls", namespace="expert")),
    path("metrics/", include("metrics.urls", namespace="metrics")),
    path("nutrition/", include("nutrition.urls", namespace="nutrition")),
    path("training/", include("training.urls", namespace="training")),
    path("chat/", include("chat.urls", namespace="chat")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
