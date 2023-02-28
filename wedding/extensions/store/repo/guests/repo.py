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
    def __init__(self, db_session: AsyncSession = Depends(db_session)):
        self._db_session = db_session

    async def save(self, guest: Guests) -> Guests:
        with self._handle_db_changes_error():
            guest = await self._db_session.merge(guest)
            await self._db_session.flush()
            return guest

    def load_query(
        self,
        guest_id: int | None = None,
    ) -> Select:
        query = select(Guests)
        if guest_id is not None:
            query = query.filter(Guests.id == guest_id)
        return query

    async def load(self, **kwargs: Any) -> list[Guests]:
        query = self.load_query(**kwargs)
        result = await self._db_session.execute(query)
        result = result.scalars()
        return cast(list[Guests], result)

    async def load_one(self, **kwargs: Any) -> Guests | None:
        query = self.load_query(**kwargs)
        result = await self._db_session.execute(query)
        result = result.scalar_one_or_none()
        return cast(Guests, result)

    async def commit(self) -> None:
        with self._handle_db_changes_error():
            await self._db_session.commit()

    @contextmanager
    def _handle_db_changes_error(self) -> Iterator[None]:
        """Контекст для того, чтобы ловить ошибки при изменении/создании записи."""
        try:
            yield
        except IntegrityError as exc:
            raise GuestsConstraintError(msg=str(exc)) from exc
