"""health_and_fitness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("consultation_signup/", include("consultation_signup.urls")),
    path("authentication/", include("authentication.urls")),
    path("personalpage/", include("personalpage.urls")),
    path("controlpage/", include("controlpage.urls")),
    path("expertpage/", include("expertpage.urls")),
    path("fatsecret_app/", include("fatsecret_app.urls")),
    path("measurements/", include("measurements.urls")),
    path("anthropometry/", include("anthropometry.urls")),
    path("client_info/", include("client_info.urls")),
    path("expert_remarks/", include("expert_remarks.urls")),
    path("expert_recommendations/", include("expert_recommendations.urls")),
    path("training/", include("training.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
