import string
from random import choice

from apps.urlinfo.services import urlinfo_service
from apps.urlinfo.types import URL, UrlInfoType


class URLInfoGenerator:
    supported_protocols = ["http", "https"]

    @staticmethod
    def generate_dummy_data(count: int = 1):
        """
        Generates test data for URLs with dummy information.
        """
        protocol = choice(URLInfoGenerator.supported_protocols)
        subdomain = "".join(choice(string.ascii_lowercase) for _ in range(5))
        domain = "".join(choice(string.ascii_lowercase) for _ in range(10))
        suffix = "".join(choice(string.ascii_lowercase) for _ in range(3))
        domain_name = f"{domain}.{suffix}"
        url = f"{protocol}://{subdomain}.{domain_name}"

        dummy_url_data = [
            UrlInfoType(
                url=url,
                protocol=protocol,
                subdomain=subdomain,
                domain_name=domain,
                title="".join(choice(string.ascii_lowercase) for _ in range(20)),
                images=[
                    f"{url}/{''.join(choice(string.ascii_lowercase) for _ in range(15))}/image.png"
                    for _ in range(8)
                ],
                stylesheets_count=choice(range(1, 11)),
            )
            for _ in range(count)
        ]
        return [urlinfo_service.create(url_info) for url_info in dummy_url_data]

    @staticmethod
    def generate_from_url(url: URL | None = None):
        """
        Generates information resources from a specific URL.
        """
        if url:
            return urlinfo_service.create_resources(url=url)
