from pydantic import BaseModel

from wedding.ctx.invitations.entity.structures import InvitationEntity, GroupEntity, GuestEntity
from wedding.extensions.rest.groups.schema import GroupSchema
from wedding.extensions.rest.guests.schema import GuestSchema


class InvitationSchema(BaseModel):
    group: GroupSchema
    guest_1: GuestSchema
    guest_2: GuestSchema | None

    @staticmethod
    def _group_schema_from_entity(entity: GroupEntity) -> GroupSchema:
        return GroupSchema(
            id=entity.id,
            name=entity.name,
            guest_1_id=entity.id,
            guest_2_id=entity.id,
            is_couple=entity.is_couple,
            form_id=entity.form_id,
        )

    @staticmethod
    def _guest_schema_from_entity(entity: GuestEntity) -> GuestSchema:
        return GuestSchema(
            id=entity.id,
            first_name=entity.first_name,
            middle_name=entity.middle_name,
            last_name=entity.last_name,
            male=entity.male.value,
            full_name=entity.full_name,
        )

    @classmethod
    def from_entity(cls, entity: InvitationEntity) -> "InvitationSchema":
        return cls(
            group=cls._group_schema_from_entity(entity=entity.group),
            guest_1=cls._guest_schema_from_entity(entity=entity.guest_1),
            guest_2=cls._guest_schema_from_entity(
                entity=entity.guest_2,
            ) if entity.guest_2 is not None else None,
        )
