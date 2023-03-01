"""Тестирование методов моделей."""
from unittest.mock import MagicMock, patch

import pytest

from tests.unit.extensions.store.repo.guests.asserts import assert_guest_model_with_entity
from tests.unit.extensions.store.repo.guests.factories import GuestsFactory
from wedding.ctx.guests.entity.guest import GuestEntity, MaleEnum


@pytest.mark.asyncio()
class TestGuests:
    """Проверка модели Guests."""

    @patch.object(GuestEntity, "cast_male")
    async def test_to_entity__happy_path(
        self,
        cast_male_mock: MagicMock,
    ):
        """Проверка преобразования модели в сущность."""
        # Arrange
        guest = await GuestsFactory()
        cast_male_mock.return_value = MaleEnum(guest.male)

        # Act
        result = guest.to_entity()

        # Asserts
        cast_male_mock.assert_called_once_with(guest.male)
        assert_guest_model_with_entity(
            model=guest,
            entity=result,
        )
