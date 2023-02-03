"""Модели необхододимые для работы с REST пользователей"""
from pydantic import BaseModel

from wedding.ctx.groups.entity.group import GroupEntity
from wedding.extensions.rest.guests.schema import GuestSchema


class GroupSchema(BaseModel):
    id: int
    name: str
    guests: list[GuestSchema]

    @classmethod
    def from_entity(cls, entity: GroupEntity) -> "GroupSchema":
        return cls(
            id=entity.id,
            name=entity.name,
            guests=[GuestSchema.from_entity(entity=guest) for guest in entity.guests],
        )
