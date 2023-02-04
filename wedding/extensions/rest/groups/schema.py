"""Модели необхододимые для работы с REST пользователей"""
from pydantic import BaseModel

from wedding.ctx.groups.dto.data import GroupData
from wedding.ctx.groups.entity.group import GroupEntity


class GroupDataSchema(BaseModel):
    name: str
    guest_1_id: int | None
    guest_2_id: int | None
    sleep_place: bool
    finalize: bool

    def to_dto(self) -> GroupData:
        return GroupData(
            name=self.name,
            guest_1_id=self.guest_1_id,
            guest_2_id=self.guest_2_id,
            sleep_place=self.sleep_place,
            finalize=self.finalize,
        )


class GroupSchema(GroupDataSchema):
    id: int
    name: str
    guest_1_id: int | None
    guest_2_id: int | None
    sleep_place: bool
    finalize: bool

    @classmethod
    def from_entity(cls, entity: GroupEntity) -> "GroupSchema":
        return cls(
            id=entity.id,
            name=entity.name,
            guest_1_id=entity.guest_1_id,
            guest_2_id=entity.guest_2_id,
            sleep_place=entity.sleep_place,
            finalize=entity.finalize,
        )
