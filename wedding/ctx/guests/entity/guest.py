from dataclasses import dataclass
from enum import Enum


class MaleEnum(Enum):
    male = "male"
    female = "female"


@dataclass
class GuestEntity:
    first_name: str
    middle_name: str | None
    last_name: str
    male: MaleEnum
    id: int = None

    @property
    def full_name(self) -> str:
        full_name_list = [self.last_name, self.first_name]
        if self.middle_name:
            full_name_list.append(self.middle_name)
        return " ".join(full_name_list)
