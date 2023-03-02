"""
Тестирование сервис для связи домена guests с хранилищем гостей

(StorageService)
"""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from faker import Faker

from tests.unit.ctx.guests.asserts import assert_guest_data_to_entity
from tests.unit.ctx.guests.factories import GuestDataFactory, GuestEntityFactory
from tests.unit.extensions.store.repo.guests.asserts import assert_guest_model_with_entity
from wedding.ctx.guests.entity.guest import GuestEntity, MaleEnum
from wedding.ctx.guests.errors import GuestEntityError, GuestNotFoundEntityError, MultipleGuestsEntityError
from wedding.ctx.guests.service.storage_service import StorageService
from wedding.ctx.guests.special_codes import GUEST_MULTIPLE_FOUND, GUEST_NOT_FOUND
from wedding.extensions.store.repo.guests.errors import GuestStoreError, MultipleGuestsFoundError
from wedding.extensions.store.repo.guests.repo import LoadGuestsFilters


@pytest.mark.asyncio()
class TestStorageService:
    """Тестирование StorageService"""

    def get_service(self, **kwargs) -> StorageService:
        service_kwargs = {"guests_repo": MagicMock()}
        service_kwargs.update(kwargs)
        return StorageService(**service_kwargs)

    @patch.object(GuestEntity, "cast_male")
    def test_create_guest_entity__happy_path(
        self,
        cast_male_mock: MagicMock,
    ):
        """Проверка создания сущности из данных гостя."""
        # Arrange
        guest_data = GuestDataFactory()
        cast_male_mock.return_value = MaleEnum(guest_data.male)

        # Act
        result = StorageService.create_guest_entity(guest_data=guest_data)

        # Asserts
        cast_male_mock.assert_called_once_with(guest_data.male)
        assert result.id is None
        assert_guest_data_to_entity(
            data=guest_data,
            entity=result,
        )

    @pytest.mark.parametrize("with_id", [True, False])
    def test_guest_entity_to_model__happy_path(
        self,
        with_id: bool,
        faker: Faker,
    ):
        """Проверка создания бд-модели из сущности гостя."""
        # Arrange
        if with_id:
            guest_id = faker.unique.pyint(min_value=1)
        else:
            guest_id = None
        guest_entity = GuestEntityFactory(id=guest_id)

        # Act
        result = StorageService.guest_entity_to_model(entity=guest_entity)

        # Asserts
        assert_guest_model_with_entity(
            model=result,
            entity=guest_entity,
        )

    async def test_get_guest_by_id__happy_path(
        self,
        faker: Faker,
    ):
        """Проверка получения гостя по идентификатору"""
        # Arrange
        guests_repo = MagicMock()
        guests_repo.load_one = AsyncMock()
        repo_result = guests_repo.load_one.return_value
        repo_result.to_entity = MagicMock()

        service = self.get_service(guests_repo=guests_repo)
        guest_id = faker.pyint(min_value=1)

        # Act
        result = await service.get_guest_by_id(guest_id=guest_id)

        # Asserts
        guests_repo.load_one.assert_called_once_with(
            filters=LoadGuestsFilters(guest_ids=[guest_id]),
        )
        repo_result.to_entity.assert_called_once_with()
        assert result == repo_result.to_entity.return_value

    async def test_get_guest_by_id__not_found(
        self,
        faker: Faker,
    ):
        """Проверка получения гостя по идентификатору"""
        # Arrange
        guests_repo = MagicMock()
        guests_repo.load_one = AsyncMock()
        guests_repo.load_one.return_value = None
        service = self.get_service(guests_repo=guests_repo)
        guest_id = faker.pyint(min_value=1)

        # Act
        with pytest.raises(GuestNotFoundEntityError) as exc:
            await service.get_guest_by_id(guest_id=guest_id)

        # Asserts
        assert exc.value.special_code == GUEST_NOT_FOUND

    @pytest.mark.parametrize(
        ("raised_error", "expected_error", "special_code"),
        [(MultipleGuestsFoundError, MultipleGuestsEntityError, GUEST_MULTIPLE_FOUND)],
    )
    async def test_get_guest_by_id__handle_errors(
        self,
        raised_error: type[GuestStoreError],
        expected_error: type[GuestEntityError],
        special_code: str,
        faker: Faker,
    ):
        """Проверка получения гостя по идентификатору"""
        # Arrange
        guests_repo = MagicMock()
        guests_repo.load_one = AsyncMock()
        guests_repo.load_one.side_effect = raised_error(msg="test")
        service = self.get_service(guests_repo=guests_repo)
        guest_id = faker.pyint(min_value=1)

        # Act
        with pytest.raises(expected_error) as exc:
            await service.get_guest_by_id(guest_id=guest_id)

        # Asserts
        assert exc.value.special_code == special_code
