"""Фабрики домена guests."""
import factory

from tests.helpers.unique_faker import UniqueFaker
from wedding.ctx.guests.dto.data import GuestData
from wedding.ctx.guests.entity.guest import GuestEntity, MaleEnum


class GuestEntityFactory(factory.Factory):
    """Фабрика для GuestEntity."""

    class Meta:
        model = GuestEntity

    first_name = factory.Faker("first_name")
    middle_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    male = factory.Faker("random_element", elements=MaleEnum)
    id = UniqueFaker("pyint")


class GuestDataFactory(factory.Factory):
    class Meta:
        model = GuestData

    first_name = factory.Faker("first_name")
    middle_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    male = factory.Faker("random_element", elements=[item.value for item in MaleEnum])
