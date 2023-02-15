from dataclasses import dataclass


@dataclass
class GuestData:
    first_name: str
    last_name: str
    male: str

    middle_name: str | None
