from dataclasses import dataclass


@dataclass
class GuestInfo:
    first_name: str
    middle_name: str
    last_name: str
    id: int = None

    @classmethod
    def from_json(cls, json_data: dict) -> "GuestInfo":
        return cls(
            first_name=json_data["first_name"],
            middle_name=json_data["middle_name"],
            last_name=json_data["last_name"],
            id=json_data["id"],
        )


@dataclass
class GroupInfo:
    id: int
    name: str
    guest_1: GuestInfo | None
    guest_2: GuestInfo | None
    finalize: bool = False

    @classmethod
    def from_json(
        cls,
        json_data: dict,
        guest_1: GuestInfo,
        guest_2: GuestInfo | None,
    ) -> "GroupInfo":
        return cls(
            id=json_data["id"],
            name=json_data["name"],
            guest_1=guest_1,
            guest_2=guest_2,
        )
