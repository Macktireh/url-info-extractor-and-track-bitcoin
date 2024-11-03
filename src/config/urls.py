from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(route=settings.DJANGO_ADMIN_PATH_NAME, view=admin.site.urls),
    path("api/v1/urlinfo/", include("apps.urlinfo.urls")),
    path("api/v1/crypto/", include("apps.crypto.urls")),
]
