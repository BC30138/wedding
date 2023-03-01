"""Тетсирование сущности гостя."""
import pytest
from faker import Faker

from tests.unit.ctx.guests.factories import GuestEntityFactory
from wedding.ctx.guests.entity.guest import GuestEntity, MaleEnum
from wedding.ctx.guests.errors import GuestEntityValidationError
from wedding.ctx.guests.special_codes import GUEST_UNRECOGNIZED_MALE


class TestGuestEntity:
    """Тестирование методов GuestEntity"""

    def test_full_name__with_middle(self):
        """Проверка генерации полного имени гостя с отчеством."""
        # Arrange
        guest = GuestEntityFactory()

        # Act
        result = guest.full_name

        # Asserts
        assert result == f"{guest.last_name} {guest.first_name} {guest.middle_name}"

    def test_full_name__without_middle(self):
        """Проверка генерации полного имени гостя без отчества."""
        # Arrange
        guest = GuestEntityFactory(middle_name=None)

        # Act
        result = guest.full_name

        # Asserts
        assert result == f"{guest.last_name} {guest.first_name}"

    def test_cast_male__happy_path(self, faker: Faker):
        """Проверка преобразования пола из строки в enum."""
        # Arrange
        male = faker.random_element(elements=MaleEnum)

        # Act
        result = GuestEntity.cast_male(value=male.value)

        # Asserts
        assert result == male

    def test_cast_male__bad_male(self, faker: Faker):
        """Проверка преобразования пола из строки в enum."""
        # Arrange
        male = faker.word()

        # Act
        with pytest.raises(GuestEntityValidationError) as exc:
            GuestEntity.cast_male(value=male)

        # Asserts
        assert exc.value.special_code == GUEST_UNRECOGNIZED_MALE
