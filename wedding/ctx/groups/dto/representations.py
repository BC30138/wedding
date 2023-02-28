from dataclasses import dataclass
from typing import cast

from wedding.ctx.groups.entity.group import GroupEntity


@dataclass
class GroupRepresentation:
    id: int
    name: str
    guest_1_id: int
    guest_2_id: int | None
    is_couple: bool
    form_id: str

    @classmethod
    def from_entity(cls, entity: GroupEntity) -> "GroupRepresentation":
        entity_id = cast(int, entity.id)
        return cls(
            id=entity_id,
            name=entity.name,
            guest_1_id=entity.guest_1_id,
            guest_2_id=entity.guest_2_id,
            is_couple=entity.is_couple,
            form_id=entity.form_id.value,
        )
