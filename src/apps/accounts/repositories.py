from apps.accounts.models import User
from apps.common.repositories.django_base_repository import DjangoBaseRepository


class UserRepository(DjangoBaseRepository[User]):
    def __init__(self, model: User) -> None:
        super().__init__(model)

    def create_superuser(self, **kwargs) -> User:
        return self.model.objects.create_superuser(**kwargs)


user_repository = UserRepository(User)
