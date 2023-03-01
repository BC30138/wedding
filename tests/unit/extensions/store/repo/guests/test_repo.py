"""Тестирование репозитория гостей."""
from typing import Any
from unittest.mock import MagicMock

import pytest
from faker import Faker
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError, IntegrityError, MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession

from tests.unit.extensions.store.repo.guests.factories import GuestsFactory, LoadGuestsFiltersFactory
from wedding.extensions.store.repo.guests.errors import GuestDBError, GuestsConstraintError, MultipleGuestsFoundError
from wedding.extensions.store.repo.guests.models import Guests
from wedding.extensions.store.repo.guests.repo import GuestsRepo


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("case_name", "filters"),
    [
        ("guest_ids", {"guest_ids": [4, 8, 15]}),
        ("all", {}),
    ],
)
async def test_load_query__happy_path(
    case_name: str,
    filters: dict[str, Any],
    db_session: AsyncSession,
    faker: Faker,
):
    """Проверка выборки для поиска гостей в базе."""
    # Arrange
    repo = GuestsRepo(db_session=db_session)
    unique_faker = faker.unique

    async def guest_ids_setup() -> set[Guests]:
        # Нет в результате выборки
        for _ in range(faker.pyint(min_value=3, max_value=10)):
            await GuestsFactory(id=unique_faker.pyint(min_value=50, max_value=100))
        # Ожидаемый результат выборки
        result = set()
        for guest_id in filters["guest_ids"]:
            result.add(await GuestsFactory(id=guest_id))
        return result

    async def all_setup() -> set[Guests]:
        # Ожидаемый результат выборки
        result = await db_session.execute(select(Guests))
        result = set(result.scalars())
        for _ in range(faker.pyint(min_value=3, max_value=10)):
            result.add(await GuestsFactory())
        return result

    setup_result = await locals()[f"{case_name}_setup"]()

    # Act
    result_query = repo.load_query(filters=filters)

    # Asserts
    result = await db_session.execute(result_query)
    result = set(result.scalars())
    assert result == setup_result


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("raised_exception", "expected_exception"),
    [(MultipleResultsFound, MultipleGuestsFoundError)],
)
async def test_handle_load_one_errors__errors(raised_exception, expected_exception):
    """Проверка хэндла ошибок при запросе данных."""
    # Arrange
    repo = GuestsRepo(db_session=MagicMock())
    filters = LoadGuestsFiltersFactory()

    # Act & Asserts
    with pytest.raises(expected_exception), repo._handle_load_one_errors(filters=filters):
        raise raised_exception()


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("raised_exception", "expected_exception"),
    [
        (IntegrityError, GuestsConstraintError),
        (DBAPIError, GuestDBError),
    ],
)
async def test_handle_changes_errors__errors(raised_exception, expected_exception):
    """Проверка хэндла ошибки, когда вернулось несколько записей."""
    # Arrange
    repo = GuestsRepo(db_session=MagicMock())

    # Act & Asserts
    with pytest.raises(expected_exception), repo._handle_changes_errors():
        raise raised_exception(
            statement=MagicMock(),
            params=MagicMock(),
            orig=MagicMock(),
        )
