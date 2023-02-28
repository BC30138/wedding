from dataclasses import dataclass
from typing import cast

from wedding.ctx.guests.entity.guest import GuestEntity


@dataclass
class GuestRepresentation:
    id: int
    first_name: str
    middle_name: str | None
    last_name: str
    male: str
    full_name: str

    @classmethod
    def from_entity(cls, guest_entity: GuestEntity) -> "GuestRepresentation":
        guest_id = cast(int, guest_entity.id)
        return cls(
            id=guest_id,
            first_name=guest_entity.first_name,
            middle_name=guest_entity.middle_name,
            last_name=guest_entity.last_name,
            male=guest_entity.male.value,
            full_name=guest_entity.full_name,
        )
