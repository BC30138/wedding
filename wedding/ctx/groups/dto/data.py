from dataclasses import dataclass


@dataclass
class GroupData:
    name: str
    sleep_place: bool = True
    finalize: bool = False
    guest_1_id: str | None = None
    guest_2_id: str | None = None
