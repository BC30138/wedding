"""Фабрики для моделей гостей."""
from factory import Faker

from tests.unit.extensions.store.factory import BaseAsyncFactory
from wedding.ctx.guests.entity.guest import MaleEnum
from wedding.extensions.store.repo.guests.models import Guests


class GuestsFactory(BaseAsyncFactory):
    """Фабрика для модели гостя Guests."""

    class Meta:
        model = Guests

    first_name = Faker("first_name")
    middle_name = Faker("first_name")
    last_name = Faker("last_name")
    male = Faker("random_element", elements=[item.value for item in MaleEnum])
