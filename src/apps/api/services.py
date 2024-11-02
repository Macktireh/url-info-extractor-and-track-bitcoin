from typing import Any, NoReturn
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from tldextract import extract as domain_extractor

from apps.api.models import URLInfo
from apps.api.repositories import URLInfoRepository, url_info_repository
from apps.api.types import URL, UrlInfoType


class URLInfoService:
    def __init__(self, url_info_repository: URLInfoRepository) -> None:
        self.url_info_repository = url_info_repository

    def get(self, id: int) -> URLInfo | None:
        return self._get_url_info(id=id)

    def get_by_public_id(self, public_id: str) -> URLInfo | None:
        return self._get_url_info(public_id=public_id)

    def create(self, payload: UrlInfoType) -> URLInfo:
        return self.url_info_repository.create(**payload)

    def create_resources(self, url: URL) -> URLInfo:
        data = self.get_resources(url)
        return self.create(data)

    def update(self, url_info: URLInfo, data: dict[str, Any]) -> URLInfo:
        return self.url_info_repository.update(url_info, **data)

    def delete(self, url_info: URLInfo) -> None:
        self.url_info_repository.delete(url_info)

    def get_resources(self, url: URL) -> UrlInfoType | NoReturn:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            result = UrlInfoType(
                url=url,
                protocol=self._get_protocol(url),
                subdomain=None,
                domain_name=None,
                title=self._get_title(soup),
                images=self._get_images(url, soup),
                stylesheets_count=len(soup.find_all("link", rel="stylesheet")),
            )
            result["subdomain"], domain, suffix = self._get_domain(url)
            result["domain_name"] = f"{domain}.{suffix}"
            return result

        except requests.RequestException as e:
            raise ValidationError(
                _("The URL is valid, but the server could not be reached and returned an error: %(error)s"),
                code="request_error",
                params={"error": str(e)},
            ) from e

    def _get_url_info(self, **kwargs) -> URLInfo | None:
        try:
            return self.url_info_repository.get(**kwargs)
        except URLInfo.DoesNotExist:
            return None

    def _get_protocol(self, url: URL) -> str:
        return urlparse(url).scheme.lower()

    def _get_domain(self, url: URL) -> tuple[str, str, str]:
        extractor = domain_extractor(url)
        return extractor.subdomain, extractor.domain, extractor.suffix

    def _get_title(self, soup: BeautifulSoup) -> str:
        title_tag = soup.find("title")
        return title_tag.text if title_tag else "No title found"

    def _get_images(self, url: URL, soup: BeautifulSoup) -> list[str]:
        protocol = self._get_protocol(url)
        full_domain_name = ".".join(self._get_domain(url))
        images = [
            img.get("src")
            if img.get("src").startswith("http")
            else f"{protocol}://{full_domain_name}{img.get('src')}"
            for img in soup.find_all("img")
            if img.get("src")
        ]
        return images


url_info_service = URLInfoService(url_info_repository=url_info_repository)
