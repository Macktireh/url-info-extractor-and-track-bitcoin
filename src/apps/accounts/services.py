from typing import Any

from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.accounts.repositories import UserRepository, user_repository


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def get(self, id: int) -> User | None:
        try:
            return self.user_repository.get(id=id)
        except User.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> User | None:
        try:
            return self.user_repository.get(email=email)
        except User.DoesNotExist:
            return None

    def get_by_public_id(self, public_id: str) -> User | None:
        try:
            return self.user_repository.get(public_id=public_id)
        except User.DoesNotExist:
            return None

    def create(self, first_name: str, last_name: str, email: str, password: str | None, **kwargs) -> User:
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.user_repository.model.objects.normalize_email(email)
        user = self.user_repository.create(first_name=first_name, last_name=last_name, email=email, **kwargs)
        if password:
            self.user_repository.set_password(user, password)
        return user

    def update(self, user: User, data: dict[str, Any]) -> User:
        return self.user_repository.update(user, **data)

    def delete(self, user: User) -> None:
        return self.user_repository.delete(user)


user_service = UserService(user_repository=user_repository)
