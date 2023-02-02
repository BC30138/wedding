from fastapi import Depends
from sqlalchemy.orm import Session
from wedding.extensions.store.database import db_session
from wedding.extensions.store.repo.users.models import Users


class UsersRepo:
    def __init__(self, db_session: Session = Depends(db_session)):
        self._db_session = db_session

    def get_by_id(self, user_id: int) -> Users:
        return self._db_session.query(Users).get(user_id)
