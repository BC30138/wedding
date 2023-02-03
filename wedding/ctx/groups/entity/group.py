from dataclasses import dataclass

from wedding.ctx.guests.entity.guest import GuestEntity


@dataclass
class GroupEntity:
    id: int
    name: str
    guests: list[GuestEntity]