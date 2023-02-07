from dataclasses import dataclass


@dataclass
class GuestEntity:
    first_name: str
    middle_name: str
    last_name: str
    group_id: int
    id: int = None
