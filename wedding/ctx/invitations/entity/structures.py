from dataclasses import dataclass

from wedding.ctx.invitations.entity.enums import MaleEnum


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
    guest_2_id: int
    is_couple: bool
    form_id: str


@dataclass
class InvitationEntity:
    group: GroupEntity
    guest_1: GuestEntity
    guest_2: GuestEntity | None = None
