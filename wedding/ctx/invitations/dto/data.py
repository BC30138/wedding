from dataclasses import dataclass


@dataclass
class GuestData:
    first_name: str
    last_name: str
    male: str

    middle_name: str | None


@dataclass
class GroupData:
    name: str


@dataclass
class InvitationDataDTO:
    group: GroupData
    guest_1: GuestData
    guest_2: GuestData | None
