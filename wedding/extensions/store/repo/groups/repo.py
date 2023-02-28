from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, cast

from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select

from wedding.extensions.store.database import db_session
from wedding.extensions.store.repo.groups.errors import GroupsConstraintError
from wedding.extensions.store.repo.groups.models import Groups


class GroupsRepo:
    def __init__(self, db_session: AsyncSession = Depends(db_session)):
        self._db_session = db_session

    async def save(self, group: Groups) -> Groups:
        with self._handle_db_changes_error():
            group = await self._db_session.merge(group)
            await self._db_session.flush()
            return group

    def load_query(
        self,
        group_id: int | None = None,
        name: int | None = None,
    ) -> Select:
        query = select(Groups)
        if group_id is not None:
            query = query.filter(Groups.id == group_id)
        if name is not None:
            query = query.filter(Groups.name == name)
        return query

    async def load_one(self, **kwargs: Any) -> Groups | None:
        query = self.load_query(**kwargs)
        result = await self._db_session.execute(query)
        result = result.scalar_one_or_none()
        return cast(Groups, result)

    async def load_all(self, **kwargs: Any) -> list[Groups]:
        query = self.load_query(**kwargs)
        result = await self._db_session.execute(query)
        result = result.scalars()
        return cast(list[Groups], result)

    async def commit(self) -> None:
        with self._handle_db_changes_error():
            await self._db_session.commit()

    @contextmanager
    def _handle_db_changes_error(self) -> Iterator[None]:
        """Контекст для того, чтобы ловить ошибки при изменении/создании записи."""
        try:
            yield
        except IntegrityError as exc:
            raise GroupsConstraintError(msg=str(exc)) from exc
