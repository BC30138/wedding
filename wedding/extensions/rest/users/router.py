"""API для работы с пользователями"""
from fastapi import APIRouter, Depends

from wedding.extensions.rest.guests.schema import Guest
from wedding.extensions.rest.users.schema import User
from wedding.extensions.store.repo.users.repo import UsersRepo

router = APIRouter(tags=["users"])


@router.get("/{user_id}")
def get_user(user_id: int) -> User:
    fake_guest = Guest(
        id=123,
        first_name="Иван",
        middle_name="Иванович",
        last_name="Иванов",
    )
    fake_user = User(
        id=user_id,
        guests=[fake_guest],
    )
    return fake_user
