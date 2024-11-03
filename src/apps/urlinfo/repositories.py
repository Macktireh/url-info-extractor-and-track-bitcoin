from apps.common.repositories.django_base_repository import DjangoBaseRepository
from apps.urlinfo.models import URLInfo


class URLInfoRepository(DjangoBaseRepository[URLInfo]):
    def __init__(self, model: URLInfo) -> None:
        super().__init__(model)


urlinfo_repository = URLInfoRepository(URLInfo)
