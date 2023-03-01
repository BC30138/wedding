"""Фэйкер для генерации уникальных значений в фабриках."""

import factory
from faker import Faker
from faker.proxy import UniqueProxy


class UniqueFaker(factory.Faker):
    """Фэйкер для генерации уникальных значений в фабриках."""

    def evaluate(self, instance, step, extra):  # noqa
        locale = extra.pop("locale")
        subfaker: Faker = self._get_faker(locale)
        unique_proxy: UniqueProxy = subfaker.unique
        return unique_proxy.format(self.provider, **extra)
