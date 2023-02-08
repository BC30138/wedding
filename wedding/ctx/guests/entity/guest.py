from dataclasses import dataclass
from enum import Enum


class MaleEnum(Enum):
    male = "male"
    female = "female"


@dataclass
class GuestEntity:
    first_name: str
    middle_name: str
    last_name: str
    group_id: int
    male: MaleEnum
    id: int = None
