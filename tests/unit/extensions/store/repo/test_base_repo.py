"""Проверка базового репозитория."""
from typing import cast
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tests.unit.extensions.store.asserts import assert_model_fields
from tests.unit.extensions.store.repo.guests.factories import GuestsFactory
from wedding.extensions.store.repo.base_repo import BaseRepo
from wedding.extensions.store.repo.guests.models import Guests


@pytest.mark.asyncio()
@pytest.mark.filterwarnings("ignore::sqlalchemy.exc.SAWarning")  # тест вызывает роллбек
@patch.object(BaseRepo, "_handle_changes_errors")
async def test_save__create(
    handle_db_changes_error_mock: MagicMock,
    db_session: AsyncSession,
):
    """Проверка создания записи в бд."""
    # Arrange
    guest_model = GuestsFactory.build()
    repo = BaseRepo(db_session=db_session)

    # Act
    result = await repo.save(model=guest_model)

    # Asserts
    handle_db_changes_error_mock.return_value.__enter__.assert_called_once_with()
    db_result = cast(Guests, await db_session.get(Guests, result.id))
    assert_model_fields(
        left_model=db_result,
        right_model=guest_model,
        exclude=("id",),
    )

    # Проверка того, что не вызывается коммит
    await db_session.rollback()
    db_result = cast(Guests, await db_session.get(Guests, result.id))
    assert db_result is None


@pytest.mark.asyncio()
@pytest.mark.filterwarnings("ignore::sqlalchemy.exc.SAWarning")  # тест вызывает роллбек
@patch.object(BaseRepo, "_handle_changes_errors")
async def test_save__update(
    _handle_db_changes_error_mock: MagicMock,
    db_session: AsyncSession,
):
    """Проверка обновления записи в бд."""
    # Arrange
    guest_model = await GuestsFactory()
    repo = BaseRepo(db_session=db_session)
    update_model = GuestsFactory.build(id=guest_model.id)

    # Act
    result = await repo.save(model=update_model)

    # Asserts
    db_result = cast(Guests, await db_session.get(Guests, guest_model.id))
    assert result == db_result
    assert_model_fields(left_model=db_result, right_model=update_model)


@pytest.mark.asyncio()
@patch.object(BaseRepo, "_handle_load_one_errors")
@patch.object(BaseRepo, "load_query")
async def test_load_one__happy_path(
    load_query_mock: MagicMock,
    handle_load_one_errors: MagicMock,
    db_session: AsyncSession,
    faker: Faker,
):
    """Проверка получения одной записи."""
    # Arrange
    repo = BaseRepo(db_session=db_session)
    guest = await GuestsFactory()
    load_query_mock.return_value = select(Guests).filter(Guests.id == guest.id)
    filters = {faker.word(): faker.word()}

    # Act
    result = await repo.load_one(filters=filters)

    # Asserts
    handle_load_one_errors.assert_called_once_with(filters=filters)
    handle_load_one_errors.return_value.__enter__.assert_called_once_with()
    load_query_mock.assert_called_once_with(filters)
    assert result == guest


@pytest.mark.asyncio()
@patch.object(BaseRepo, "_handle_changes_errors")
async def test_commit__happy_path(
    handle_db_changes_error_mock: MagicMock,
):
    """Проверка вызова коммита."""
    # Arrange
    session_mock = MagicMock()
    session_mock.commit = AsyncMock()
    repo = BaseRepo(db_session=session_mock)

    # Act
    await repo.commit()

    # Asserts
    handle_db_changes_error_mock.return_value.__enter__.assert_called_once_with()
    session_mock.commit.assert_called_once_with()
