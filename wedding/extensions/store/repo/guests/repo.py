from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from wedding.extensions.store.database import db_session
from wedding.extensions.store.global_errors import ConstraintError
from wedding.extensions.store.repo.guests.errors import GuestsConstraintError
from wedding.extensions.store.repo.guests.models import Guests


class GuestsRepo:
    def __init__(self, db_session: AsyncSession = Depends(db_session)):
        self._db_session = db_session

    def load_query(
        self,
        guest_id: int | None = None,
    ) -> Select:
        query = select(Guests)
        if guest_id is not None:
            query = query.filter(Guests.id == guest_id)
        return query

    async def load(self, **kwargs) -> list[Guests]:
        query = self.load_query(**kwargs)
        result = await self._db_session.execute(query)
        return result.scalars()

    async def load_one(self, **kwargs) -> Guests | None:
        query = self.load_query(**kwargs)
        result = await self._db_session.execute(query)
        return result.scalar_one_or_none()

    async def save(self, guest: Guests) -> Guests:
        try:
            guest = await self._db_session.merge(guest)
            await self._db_session.commit()
            return guest
        except IntegrityError as exc:
            raise GuestsConstraintError(msg=str(exc)) from exc
