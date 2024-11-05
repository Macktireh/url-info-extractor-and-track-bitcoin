from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path(route=settings.DJANGO_ADMIN_PATH_NAME, view=admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("api/v1/urlinfo/", include("apps.urlinfo.urls")),
    path("api/v1/crypto/", include("apps.crypto.urls")),
]
