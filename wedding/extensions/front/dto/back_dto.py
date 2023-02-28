from dataclasses import dataclass
from enum import Enum
from typing import Any


class GroupPronounEnum(Enum):
    he = "he"
    she = "she"
    they = "they"


@dataclass
class GuestInfo:
    full_name: str
    male: str
    id: int

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> "GuestInfo":
        return cls(
            full_name=json_data["full_name"],
            male=json_data["male"],
            id=json_data["id"],
        )


@dataclass
class GroupInfo:
    id: int
    name: str
    is_couple: bool
    form_id: str
    guest_1: GuestInfo
    guest_2: GuestInfo | None

    @property
    def pronoun(self) -> GroupPronounEnum:
        if self.is_couple:
            return GroupPronounEnum.they
        elif self.guest_1.male == "male":
            return GroupPronounEnum.he
        else:
            return GroupPronounEnum.she

    @classmethod
    def from_json(
        cls,
        json_data: dict[str, Any],
        guest_1: GuestInfo,
        guest_2: GuestInfo | None,
    ) -> "GroupInfo":
        return cls(
            id=json_data["id"],
            name=json_data["name"],
            guest_1=guest_1,
            guest_2=guest_2,
            is_couple=json_data["is_couple"],
            form_id=json_data["form_id"],
        )
