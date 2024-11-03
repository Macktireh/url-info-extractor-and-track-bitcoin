from http import HTTPStatus
from typing import Any

from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.crypto.services import CryptoBitcoinService


class CryptoBitcoinView(APIView):
    def get(self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        try:
            crypto_service = CryptoBitcoinService()
            data = crypto_service.get_bitcoin_data()
            return Response(
                data,
                status=HTTPStatus.OK,
            )
        except Exception as e:
            return Response(
                {
                    "detail": f"An error occurred while retrieving Bitcoin data: {e}",
                },
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
