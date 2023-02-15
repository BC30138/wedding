from dataclasses import dataclass


@dataclass
class GroupData:
    name: str
    guest_1_id: int
    guest_2_id: int | None = None
