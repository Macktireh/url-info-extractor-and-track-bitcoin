from http import HTTPStatus

from rest_framework.exceptions import APIException


class UnprocessableEntityException(APIException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY


class ConflictException(APIException):
    status_code = HTTPStatus.CONFLICT


class InternalServerException(APIException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR


class BadGatewayException(APIException):
    status_code = HTTPStatus.BAD_GATEWAY


class GatewayTimeoutException(APIException):
    status_code = HTTPStatus.GATEWAY_TIMEOUT
