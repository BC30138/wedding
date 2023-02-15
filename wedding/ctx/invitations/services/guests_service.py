from fastapi import Depends

from wedding.ctx.guests.dto.representations import GuestRepresentation
from wedding.ctx.guests.handler.create_guest_handler import CreateGuestHandler
from wedding.ctx.invitations.dto.data import GuestData
from wedding.ctx.guests.dto.data import GuestData as DomainGuestData
from wedding.ctx.invitations.entity.enums import MaleEnum
from wedding.ctx.invitations.entity.structures import GuestEntity, InvitationEntity


class GuestsService:
    def __init__(
        self,
        create_guest_api: CreateGuestHandler = Depends(CreateGuestHandler),
    ):
        self._create_guest_api = create_guest_api

    @staticmethod
    def create_entity_from_representation(
        representation: GuestRepresentation
    ) -> GuestEntity:
        return GuestEntity(
            id=representation.id,
            first_name=representation.first_name,
            middle_name=representation.middle_name,
            last_name=representation.last_name,
            male=MaleEnum(representation.male),
            full_name=representation.full_name,
        )

    async def create_guest(self, guest_data: GuestData) -> GuestEntity:
        domain_guest_data = DomainGuestData(
            first_name=guest_data.first_name,
            middle_name=guest_data.middle_name,
            last_name=guest_data.last_name,
            male=guest_data.male,
        )
        guest_representation = await self._create_guest_api.create_by_dto_return_representation(
            guest_data=domain_guest_data,
            db_commit=False,
        )
        return self.create_entity_from_representation(
            representation=guest_representation,
        )

