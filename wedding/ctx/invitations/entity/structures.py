from dataclasses import dataclass
from urllib.parse import urlparse

from wedding.ctx.invitations.entity.enums import MaleEnum
from wedding.ctx.invitations.entity.vars import BASE_INVITATION_PATH


@dataclass
class GuestEntity:
    id: int
    first_name: str
    middle_name: str | None
    last_name: str
    male: MaleEnum
    full_name: str


@dataclass
class GroupEntity:
    id: int
    name: str
    guest_1_id: int
    guest_2_id: int | None
    is_couple: bool
    form_id: str


@dataclass
class InvitationEntity:
    group: GroupEntity
    guest_1: GuestEntity
    guest_2: GuestEntity | None = None


@dataclass
class ShareInvitationEntity:
    group_name: str
    guest_1_full_name: str
    guest_2_full_name: str | None
    link: str

    @classmethod
    def from_entities(
        cls,
        group: GroupEntity,
        guest_1: GuestEntity,
        guest_2: GuestEntity | None,
        base_url: str,
    ) -> "ShareInvitationEntity":
        base_url_obj = urlparse(base_url)
        base_url = str(base_url_obj.netloc)
        base_url = base_url.encode().decode("idna")

        return cls(
            group_name=group.name,
            guest_1_full_name=guest_1.full_name,
            guest_2_full_name=guest_2.full_name if guest_2 else None,
            link=f"{base_url}/{BASE_INVITATION_PATH}/{group.id}",
        )
