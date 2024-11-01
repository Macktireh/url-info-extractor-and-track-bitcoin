from django.http import HttpRequest

from apps.accounts.models import User


class AuthenticatedHttpRequest(HttpRequest):
    user: User
