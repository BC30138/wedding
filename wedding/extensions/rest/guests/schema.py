"""Модели необход"""
from pydantic import BaseModel


class Guest(BaseModel):
    id: int
    first_name: str
    middle_name: str
    last_name: str
