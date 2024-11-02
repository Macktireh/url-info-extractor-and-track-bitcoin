from apps.api.models import URLInfo
from apps.common.repositories.django_base_repository import DjangoBaseRepository


class URLInfoRepository(DjangoBaseRepository[URLInfo]):
    def __init__(self, model: URLInfo) -> None:
        super().__init__(model)


url_info_repository = URLInfoRepository(URLInfo)
