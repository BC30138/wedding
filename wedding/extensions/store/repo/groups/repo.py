from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from wedding.extensions.store.database import db_session
from wedding.extensions.store.repo.groups.models import Groups
from sqlalchemy.future import select


class GroupsRepo:
    def __init__(self, db_session: AsyncSession = Depends(db_session)):
        self._db_session = db_session

    async def get_by_id(self, group_id: int) -> Groups | None:
        return await self._db_session.get(
            Groups,
            group_id,
            options=[selectinload(Groups.guests)],
        )
