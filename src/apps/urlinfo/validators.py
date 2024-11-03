from http import HTTPStatus

import requests
from django.core.validators import URLValidator as DjangoURLValidator
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.validators import UniqueValidator as RestUniqueValidator

from apps.common.exceptions import ConflictError, UnprocessableEntityError


class UniqueValidator(RestUniqueValidator):
    def __call__(self, value, serializer_field) -> None:
        try:
            super().__call__(value, serializer_field)
        except RestValidationError as e:
            raise ConflictError(e.detail) from e


class URLValidator(DjangoURLValidator):
    schemes = ["http", "https"]


class URLStatusValidator(URLValidator):
    def __call__(self, value) -> None:
        super().__call__(value)

        try:
            response = requests.head(url=value)
            if response.status_code != HTTPStatus.OK:
                raise UnprocessableEntityError(
                    _(f"The URL is valid, but returned an unsuccessful status code: {response.status_code}"),
                )
        except requests.RequestException as e:
            raise UnprocessableEntityError(
                _(f"The URL is valid, but the server could not be reached and returned an error: {e}"),
            ) from e
