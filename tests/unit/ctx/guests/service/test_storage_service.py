"""
Тестирование сервис для связи домена guests с хранилищем гостей

(StorageService)
"""
from unittest.mock import MagicMock, patch

import pytest
from faker import Faker

from tests.unit.ctx.guests.asserts import assert_guest_data_to_entity
from tests.unit.ctx.guests.factories import GuestDataFactory, GuestEntityFactory
from tests.unit.extensions.store.repo.guests.asserts import assert_guest_model_with_entity
from wedding.ctx.guests.entity.guest import GuestEntity, MaleEnum
from wedding.ctx.guests.service.storage_service import StorageService


@pytest.mark.asyncio()
class TestStorageService:
    """Тестирование StorageService"""

    def get_service(self, **kwargs) -> StorageService:
        service_kwargs = {"guests_repo": MagicMock()}
        service_kwargs.update(kwargs)
        return StorageService(**service_kwargs)

    @patch.object(GuestEntity, "cast_male")
    async def test_create_guest_entity__happy_path(
        self,
        cast_male_mock: MagicMock,
    ):
        """Проверка создания сущности из данных гостя."""
        # Arrange
        service = self.get_service()
        guest_data = GuestDataFactory()
        cast_male_mock.return_value = MaleEnum(guest_data.male)

        # Act
        result = service.create_guest_entity(guest_data=guest_data)

        # Asserts
        cast_male_mock.assert_called_once_with(guest_data.male)
        assert result.id is None
        assert_guest_data_to_entity(
            data=guest_data,
            entity=result,
        )

    @pytest.mark.parametrize("with_id", [True, False])
    async def test_guest_entity_to_model__happy_path(
        self,
        with_id: bool,
        faker: Faker,
    ):
        """Проверка создания бд-модели из сущности гостя."""
        # Arrange
        service = self.get_service()
        if with_id:
            guest_id = faker.unique.pyint(min_value=1)
        else:
            guest_id = None
        guest_entity = GuestEntityFactory(id=guest_id)

        # Act
        result = service.guest_entity_to_model(entity=guest_entity)

        # Asserts
        assert_guest_model_with_entity(
            model=result,
            entity=guest_entity,
        )
