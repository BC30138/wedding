"""Тестирование методов моделей."""
import pytest
from faker import Faker

from tests.unit.extensions.store.repo.guests.asserts import assert_guest_model_with_entity
from tests.unit.extensions.store.repo.guests.factories import GuestsFactory
from wedding.ctx.guests.errors import GuestEntityValidationError
from wedding.ctx.guests.special_codes import GUEST_UNRECOGNIZED_MALE


@pytest.mark.asyncio()
class TestGuests:
    """Проверка модели Guests."""

    async def test_to_entity__happy_path(self):
        """Проверка преобразования модели в сущность."""
        # Arrange
        guest = await GuestsFactory()

        # Act
        result = guest.to_entity()

        # Asserts
        assert_guest_model_with_entity(
            model=guest,
            entity=result,
        )

    async def test_to_entity__bad_male(
        self,
        faker: Faker,
    ):
        """
        Проверка преобразования модели в сущность,
        когда передано некорректное значение male.
        """
        # Arrange
        guest = await GuestsFactory(male=faker.word())

        # Act
        with pytest.raises(GuestEntityValidationError) as exc:
            guest.to_entity()

        # Asserts
        assert exc.value.special_code == GUEST_UNRECOGNIZED_MALE
