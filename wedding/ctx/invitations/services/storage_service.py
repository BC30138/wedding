from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from wedding.extensions.store.database import db_session


class StorageService:
    def __init__(self, db_session: AsyncSession = Depends(db_session)):
        self._db_session = db_session

    def commit(self):
        self._db_session.commit()
