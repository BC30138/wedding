"""Модели необход"""
from pydantic import BaseModel

from wedding.ctx.guests.dto.data import GuestData
from wedding.ctx.guests.entity.guest import GuestEntity


class GuestDataSchema(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    group_id: int

    def to_dto(self) -> GuestData:
        return GuestData(
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name,
            group_id=self.group_id,
        )


class GuestSchema(GuestDataSchema):
    id: int

    @classmethod
    def from_entity(cls, entity: GuestEntity) -> "GuestSchema":
        return cls(
            id=entity.id,
            first_name=entity.first_name,
            middle_name=entity.middle_name,
            last_name=entity.last_name,
            group_id=entity.group_id,
        )
