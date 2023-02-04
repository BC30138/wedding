from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from wedding.extensions.store.database import db_session
from wedding.extensions.store.repo.groups.models import Groups


class GroupsRepo:
    def __init__(self, db_session: AsyncSession = Depends(db_session)):
        self._db_session = db_session

    def load_query(
        self,
        group_id: int | None,
        name: int | None,
    ) -> Select:
        query = select(Groups)
        if group_id is not None:
            query = query.filter(Groups.id == group_id)
        if name is not None:
            query = query.filter(Groups.name == name)
        return query

    async def load_one(self, **kwargs) -> Groups | None:
        query = self.load_query(**kwargs)
        result = await self._db_session.execute(query)
        return result.scalar_one_or_none()

    async def save(self, group: Groups) -> Groups:
        try:
            group = await self._db_session.merge(group)
            await self._db_session.commit()
            return group
        except IntegrityError as exc:
            print(exc.orig.__context__)

