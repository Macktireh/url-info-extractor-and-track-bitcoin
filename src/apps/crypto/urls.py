from django.urls import path

from apps.crypto.views import CryptoBitcoinView

urlpatterns = [
    path(route="bitcoin/", view=CryptoBitcoinView.as_view(), name="bitcoin"),
]
