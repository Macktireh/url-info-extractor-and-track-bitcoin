from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as AuthGroup
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers import UserManager
from apps.common.models import BaseModel


class User(BaseModel, AbstractUser):
    username = None
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True, db_index=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return f"{self.get_full_name()}<{self.email}>"


class Group(AuthGroup):
    class Meta:
        proxy = True
