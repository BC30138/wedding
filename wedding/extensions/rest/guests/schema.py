"""Модели необход"""
from pydantic import BaseModel

from wedding.ctx.guests.entity.guest import GuestEntity


class GuestSchema(BaseModel):
    id: int
    first_name: str
    middle_name: str
    last_name: str
    group_id: int

    @classmethod
    def from_entity(cls, entity: GuestEntity) -> "GuestSchema":
        return cls(
            id=entity.id,
            first_name=entity.first_name,
            middle_name=entity.middle_name,
            last_name=entity.last_name,
            group_id=entity.group_id,
        )
