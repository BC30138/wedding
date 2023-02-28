"""Тестирование репозитория гостей."""
from typing import cast
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.unit.extensions.store.repo.guests.factories import GuestsFactory
from wedding.extensions.store.repo.guests.models import Guests
from wedding.extensions.store.repo.guests.repo import GuestsRepo


def assert_data_fields(left_model: Guests, right_model: Guests):
    assert left_model.male == right_model.male
    assert left_model.first_name == right_model.first_name
    assert left_model.middle_name == right_model.middle_name
    assert left_model.last_name == right_model.last_name


@pytest.mark.asyncio()
@pytest.mark.filterwarnings("ignore::sqlalchemy.exc.SAWarning")  # тест вызывает роллбек
@patch.object(GuestsRepo, "_handle_db_changes_error")
async def test_save__happy_path(
    handle_db_changes_error_mock: MagicMock,
    db_session: AsyncSession,
):
    """Проверка сохранения гостя в бд."""
    # Arrange
    guest_model = GuestsFactory.build_model(first_name="aaa")
    repo = GuestsRepo(db_session=db_session)

    # Act
    result = await repo.save(guest=guest_model)

    # Asserts
    handle_db_changes_error_mock.return_value.__enter__.assert_called_once_with()
    assert result.id is not None
    db_result = cast(Guests, await db_session.get(Guests, result.id))
    assert db_result is not None
    assert_data_fields(
        left_model=db_result,
        right_model=guest_model,
    )

    # Проверка того, что не вызывается коммит
    await db_session.rollback()
    db_result = cast(Guests, await db_session.get(Guests, result.id))
    assert db_result is None
