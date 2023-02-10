"""Сущность группы гостей."""
from dataclasses import dataclass
from enum import Enum


class FormIdEnum(Enum):
    single = "63e670163e9d085236bbadb0"
    couple = "63e66e03505690513af610f1"


@dataclass
class GroupEntity:
    name: str
    guest_1_id: int | None
    guest_2_id: int | None
    id: int = None

    @property
    def is_couple(self) -> bool:
        if self.guest_2_id:
            return True
        else:
            return False

    @property
    def form_id(self) -> FormIdEnum:
        if self.is_couple:
            return FormIdEnum.couple
        else:
            return FormIdEnum.single
