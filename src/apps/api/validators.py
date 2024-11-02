from http import HTTPStatus

import requests
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator as DjangoURLValidator
from django.utils.translation import gettext_lazy as _


class URLValidator(DjangoURLValidator):
    schemes = ["http", "https"]


class URLStatusValidator(URLValidator):
    def __call__(self, value) -> None:
        super().__call__(value)

        try:
            response = requests.head(url=value)
            if response.status_code != HTTPStatus.OK:
                raise ValidationError(
                    _("The URL is valid, but returned an unsuccessful status code: %(status_code)s"),
                    code="status_code_error",
                    params={"value": value, "status_code": response.status_code},
                )
        except requests.RequestException as e:
            raise ValidationError(
                _("The URL is valid, but the server could not be reached and returned an error: %(error)s"),
                code="request_error",
                params={"value": value, "error": str(e)},
            ) from e
