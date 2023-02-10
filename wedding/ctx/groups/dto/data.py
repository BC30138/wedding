from dataclasses import dataclass


@dataclass
class GroupData:
    name: str
    guest_1_id: str | None = None
    guest_2_id: str | None = None
