"""Фабрики для бд гостей."""
from random import randint

import factory

from tests.helpers.unique_faker import UniqueFaker
from tests.unit.extensions.store.factory import BaseAsyncFactory
from wedding.ctx.guests.entity.guest import MaleEnum
from wedding.extensions.store.repo.guests.models import Guests
from wedding.extensions.store.repo.guests.repo import LoadGuestsFilters


class GuestsFactory(BaseAsyncFactory):
    """Фабрика для модели гостя Guests."""

    class Meta:
        model = Guests

    first_name = factory.Faker("first_name")
    middle_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    male = factory.Faker("random_element", elements=[item.value for item in MaleEnum])


class LoadGuestsFiltersFactory(factory.Factory):
    """Фабрика для фильтра гостей LoadGuestsFilters."""

    class Meta:
        model = LoadGuestsFilters

    guest_ids = factory.List([UniqueFaker("pyint", min_value=1) for _ in range(randint(1, 10))])
