from http import HTTPStatus

from rest_framework.exceptions import APIException


class UnprocessableEntityError(APIException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY


class ConflictError(APIException):
    status_code = HTTPStatus.CONFLICT
