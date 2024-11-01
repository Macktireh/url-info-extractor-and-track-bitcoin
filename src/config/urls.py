from django.conf import settings
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path(route=settings.DJANGO_ADMIN_PATH_NAME, view=admin.site.urls),
]
