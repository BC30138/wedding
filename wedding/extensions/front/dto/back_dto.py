from dataclasses import dataclass
from enum import Enum


class GuestMaleEnum(Enum):
    male = "male"
    female = "female"
    they = "they"


@dataclass
class GuestInfo:
    first_name: str
    middle_name: str
    last_name: str
    male: GuestMaleEnum
    id: int = None

    @classmethod
    def from_json(cls, json_data: dict) -> "GuestInfo":
        return cls(
            first_name=json_data["first_name"],
            middle_name=json_data["middle_name"],
            last_name=json_data["last_name"],
            male=GuestMaleEnum(json_data["male"]),
            id=json_data["id"],
        )

    @property
    def full_name(self) -> str:
        full_name_list = [self.last_name, self.first_name]
        if self.middle_name:
            full_name_list.append(self.middle_name)
        return " ".join(full_name_list)


@dataclass
class GroupInfo:
    id: int
    name: str
    guest_1: GuestInfo | None
    guest_2: GuestInfo | None
    finalize: bool = False

    @classmethod
    def from_json(
        cls,
        json_data: dict,
        guest_1: GuestInfo,
        guest_2: GuestInfo | None,
    ) -> "GroupInfo":
        return cls(
            id=json_data["id"],
            name=json_data["name"],
            guest_1=guest_1,
            guest_2=guest_2,
        )

    @property
    def male(self) -> GuestMaleEnum:
        if self.guest_2:
            return GuestMaleEnum.they
        else:
            return GuestMaleEnum(self.guest_1.male.value)
