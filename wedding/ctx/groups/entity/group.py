"""Сущность группы гостей."""
from dataclasses import dataclass


@dataclass
class GroupEntity:
    name: str
    guest_1_id: int | None
    guest_2_id: int | None
    id: int = None
    sleep_place: bool = True
    finalize: bool = False
