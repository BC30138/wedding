"""Модели необхододимые для работы с REST пользователей"""
from pydantic import BaseModel

from wedding.extensions.rest.guests.schema import Guest


class User(BaseModel):
    id: int
    guests: list[Guest]
