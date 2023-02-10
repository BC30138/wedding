"""Модели необхододимые для работы с REST пользователей"""
from pydantic import BaseModel

from wedding.ctx.groups.dto.data import GroupData
from wedding.ctx.groups.entity.group import GroupEntity


class GroupDataSchema(BaseModel):
    name: str
    guest_1_id: int | None
    guest_2_id: int | None

    def to_dto(self) -> GroupData:
        return GroupData(
            name=self.name,
            guest_1_id=self.guest_1_id,
            guest_2_id=self.guest_2_id,
        )


class GroupSchema(GroupDataSchema):
    id: int
    is_couple: bool
    form_id: str

    @classmethod
    def from_entity(cls, entity: GroupEntity) -> "GroupSchema":
        return cls(
            id=entity.id,
            name=entity.name,
            guest_1_id=entity.guest_1_id,
            guest_2_id=entity.guest_2_id,
            is_couple=entity.is_couple,
            form_id=entity.form_id.value,
        )
