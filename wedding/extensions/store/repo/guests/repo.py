"""Репозиторий для доступа к данным гостей."""
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, cast

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select

from wedding.extensions.store.database import db_session
from wedding.extensions.store.repo.guests.errors import GuestsConstraintError
from wedding.extensions.store.repo.guests.models import Guests


class GuestsRepo:
    """Репозиторий для доступа к данным гостей."""

    def __init__(self, db_session: AsyncSession = Depends(db_session)):
        self._db_session = db_session

    async def save(self, guest: Guests) -> Guests:
        """
        Сохраняет/обновляет гостя в бд

        :param guest: модель гостя, которого нужно сохранить/обновить
        :return: созданная/обновленная модель гостя
        """
        with self._handle_db_changes_error():
            guest = await self._db_session.merge(guest)
            await self._db_session.flush()
            return guest

    def load_query(
        self,
        guest_id: int | None = None,
    ) -> Select:
        """
        Создает выборку для поиска гостей

        :param guest_id: идентификатор гостя
        :return: выборка для поиска гостей
        """
        query = select(Guests)
        if guest_id is not None:
            query = query.filter(Guests.id == guest_id)
        return query

    async def load_one(self, **kwargs: Any) -> Guests | None:
        """Ищет одного гостя в бд."""
        query = self.load_query(**kwargs)
        result = await self._db_session.execute(query)
        result = result.scalar_one_or_none()
        return cast(Guests, result)

    async def commit(self) -> None:
        """Коммитит изменения в бд."""
        with self._handle_db_changes_error():
            await self._db_session.commit()

    @contextmanager
    def _handle_db_changes_error(self) -> Iterator[None]:
        """Контекст для того, чтобы ловить ошибки при изменении/создании записи."""
        try:
            yield
        except IntegrityError as exc:
            raise GuestsConstraintError(msg=str(exc)) from exc
