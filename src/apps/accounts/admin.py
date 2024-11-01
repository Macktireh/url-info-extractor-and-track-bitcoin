from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as AuthGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as AuthGroup
from django.forms import Form, ValidationError
from django.utils.translation import gettext_lazy as _

from apps.accounts.forms import UserChangeForm, UserCreationForm
from apps.accounts.models import Group, User
from apps.accounts.services import user_service
from apps.common.types import AuthenticatedHttpRequest


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "email",
        "full_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
        "updated_at",
    )
    list_filter = (
        "is_superuser",
        "is_staff",
        "is_active",
        "date_joined",
        "updated_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "public_id",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "updated_at",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )
    readonly_fields = ("public_id", "date_joined", "last_login", "updated_at")
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    ordering = ("date_joined",)

    def save_model(self, request: AuthenticatedHttpRequest, obj: User, form: Form, change: bool) -> None:
        if change:
            return super().save_model(request, obj, form, change)

        try:
            payload = form.cleaned_data
            payload.pop("password2")
            payload["password"] = payload.pop("password1")
            user_service.create(**payload)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)

    def full_name(self, obj: User) -> str:
        return obj.get_full_name()


admin.site.unregister(AuthGroup)


@admin.register(Group)
class GroupAdmin(AuthGroupAdmin):
    pass
