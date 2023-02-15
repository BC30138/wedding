from dataclasses import dataclass

from wedding.ctx.groups.entity.group import GroupEntity


@dataclass
class GroupRepresentation:
    id: int
    name: str
    guest_1_id: int
    guest_2_id: int
    is_couple: bool
    form_id: str

    @classmethod
    def from_entity(
        cls,
        entity: GroupEntity
    ) -> "GroupRepresentation":
        return cls(
            id=entity.id,
            name=entity.name,
            guest_1_id=entity.guest_1_id,
            guest_2_id=entity.guest_2_id,
            is_couple=entity.is_couple,
            form_id=entity.form_id.value,
        )
