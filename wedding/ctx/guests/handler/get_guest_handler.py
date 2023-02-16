from fastapi import Depends

from wedding.ctx.guests.dto.representations import GuestRepresentation
from wedding.ctx.guests.use_case.get_guest import GetGuestUseCase
from wedding.extensions.rest.guests.schema import GuestSchema


class GetGuestHandler:
    def __init__(self, use_case: GetGuestUseCase = Depends(GetGuestUseCase)):
        self._use_case = use_case

    async def get_by_return_schema(self, guest_id: int) -> GuestSchema:
        guest = await self._use_case.execute(guest_id=guest_id)
        return GuestSchema.from_entity(entity=guest)

    async def get_by_return_representation(self, guest_id: int) -> GuestRepresentation:
        guest = await self._use_case.execute(guest_id=guest_id)
        return GuestRepresentation.from_entity(guest_entity=guest)
