from typing import NewType, Required, TypedDict

URL = NewType("URL", str)


class UrlInfoType(TypedDict):
    url: Required[URL]
    domain_name: Required[str]
    subdomain: str | None
    protocol: Required[str]
    title: Required[str]
    images: list[URL] | None
    stylesheets_count: int
