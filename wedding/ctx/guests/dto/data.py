from dataclasses import dataclass


@dataclass
class GuestData:
    first_name: str
    middle_name: str
    last_name: str
    group_id: int
