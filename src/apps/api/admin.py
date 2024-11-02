from copy import deepcopy
from typing import Any

from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.forms import Form

from apps.api.models import URLInfo
from apps.api.services import url_info_service
from apps.common.types import AuthenticatedHttpRequest


@admin.register(URLInfo)
class URLInfoAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "protocol",
        "subdomain",
        "domain_name",
        "title",
        "images",
        "stylesheets_count",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "protocol",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "url",
                    "protocol",
                    "subdomain",
                    "domain_name",
                    "title",
                    "images",
                    "stylesheets_count",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")
    search_fields = (
        "url",
        "subdomain",
        "domain_name",
        "title",
    )
    ordering = ("created_at",)

    def get_fieldsets(self, request, obj=None) -> list[tuple[str | None, dict[str, Any]]]:
        """Custom override to exclude fields"""
        fieldsets = deepcopy(super().get_fieldsets(request, obj))

        # Append excludes here instead of using self.exclude.
        # When fieldsets are defined for the user admin, so self.exclude is ignored.
        exclude = ()

        if "add" in request.path.split("/"):
            exclude += (
                "protocol",
                "subdomain",
                "domain_name",
                "title",
                "images",
                "stylesheets_count",
                "created_at",
                "updated_at",
            )

        # Iterate fieldsets
        for fieldset in fieldsets:
            fieldset_fields = fieldset[1]["fields"]

            # Remove excluded fields from the fieldset
            for exclude_field in exclude:
                if exclude_field in fieldset_fields:
                    fieldset_fields = tuple(field for field in fieldset_fields if field != exclude_field)
                    fieldset[1]["fields"] = fieldset_fields

        return fieldsets

    def save_model(self, request: AuthenticatedHttpRequest, obj: URLInfo, form: Form, change: bool) -> None:
        if change:
            return super().save_model(request, obj, form, change)
        try:
            url_info_service.create_resources(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)
