from dataclasses import dataclass


@dataclass
class GuestEntity:
    id: int
    first_name: str
    middle_name: str
    last_name: str
    group_id: int
