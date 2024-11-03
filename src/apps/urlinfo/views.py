from http import HTTPStatus
from typing import Any

from django.http import HttpRequest
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.urlinfo.serializers import URLInfoCreationSerializer, URLInfoOutputSerializer
from apps.urlinfo.services import urlinfo_service


class URLInfoApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        serializer = URLInfoCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        urlinfo_service.create_resources(**serializer.validated_data)

        return Response(
            {
                "detail": "The URL info has been successfully created",
            },
            status=HTTPStatus.CREATED,
        )

    def get(self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        urls_info = urlinfo_service.all()
        serializer = URLInfoOutputSerializer(urls_info, many=True)
        return Response(serializer.data)


class URLInfoDetailByPublicIdApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        public_id = kwargs["public_id"]
        url_info = urlinfo_service.get_by_public_id(public_id)
        if not url_info:
            return Response(
                {
                    "detail": "The URL info does not exist",
                },
                status=HTTPStatus.NOT_FOUND,
            )
        serializer = URLInfoOutputSerializer(url_info)
        return Response(serializer.data)

    def delete(self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        public_id = kwargs["public_id"]
        url_info = urlinfo_service.get_by_public_id(public_id)
        if not url_info:
            return Response(
                {
                    "detail": "The URL info does not exist",
                },
                status=HTTPStatus.NOT_FOUND,
            )
        urlinfo_service.delete(url_info)
        return Response(
            {
                "detail": "The URL info has been successfully deleted",
            },
            status=HTTPStatus.NO_CONTENT,
        )


class URLInfoDetailByUrlApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        url = request.GET.get("url")
        url_info = urlinfo_service.get(url=url)
        if not url_info:
            return Response(
                {
                    "detail": "The URL info does not exist",
                },
                status=HTTPStatus.NOT_FOUND,
            )
        serializer = URLInfoOutputSerializer(url_info)
        return Response(serializer.data)

    def delete(self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Response:
        url = request.GET.get("url")
        url_info = urlinfo_service.get(url=url)
        if not url_info:
            return Response(
                {
                    "detail": "The URL info does not exist",
                },
                status=HTTPStatus.NOT_FOUND,
            )
        urlinfo_service.delete(url_info)
        return Response(
            {
                "detail": "The URL info has been successfully deleted",
            },
            status=HTTPStatus.NO_CONTENT,
        )
