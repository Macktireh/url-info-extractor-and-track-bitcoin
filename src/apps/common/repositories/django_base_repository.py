from typing import Any, Generic, TypeVar

from django.db.models import Model
from django.db.models.manager import BaseManager

from apps.common.repositories.base_repository import BaseRepository

T = TypeVar("T", bound=Model)


class DjangoBaseRepository(BaseRepository, Generic[T]):
    def __init__(self, model: type[T]) -> None:
        self.model = model

    def save(self, instance: T) -> T:
        instance.save()
        return instance

    def create(self, **kwargs: dict[str, Any]) -> T:
        return self.model.objects.create(**kwargs)

    def get(self, **kwargs: dict[str, Any]) -> T | None:
        return self.model.objects.get(**kwargs)

    def all(self) -> BaseManager[T]:
        return self.model.objects.all()

    def filter(self, **kwargs: dict[str, Any]) -> BaseManager[T]:
        return self.model.objects.filter(**kwargs)

    def delete(self, instance: T) -> None:
        instance.delete()

    def update(self, instance: T, **kwargs: dict[str, Any]) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return self.save(instance)

    def get_or_create(self, **kwargs: dict[str, Any]) -> tuple[T, bool]:
        return self.model.objects.get_or_create(**kwargs)

    def update_or_create(self, **kwargs: dict[str, Any]) -> tuple[T, bool]:
        return self.model.objects.update_or_create(**kwargs)

    def bulk_create(self, instances: list[T]) -> list[T]:
        return self.model.objects.bulk_create(instances)

    def bulk_update(self, instances: list[T], fields: list[str]) -> list[T]:
        return self.model.objects.bulk_update(instances, fields)

    def set_password(self, user: T, password: str) -> None:
        user.set_password(password)
        user.save()
