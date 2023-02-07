from fastapi import Depends

from wedding.ctx.guests.use_case.create_guest import CreateGuestUseCase
from wedding.extensions.rest.guests.schema import GuestDataSchema, GuestSchema


class CreateGuestHandler:
    def __init__(self, use_case: CreateGuestUseCase = Depends(CreateGuestUseCase)):
        self._use_case = use_case

    async def create_by_schema_return_schema(self, guest_data_schema: GuestDataSchema) -> GuestSchema:
        guest_data = guest_data_schema.to_dto()
        guest = await self._use_case.execute(guest_data=guest_data)
        return GuestSchema.from_entity(entity=guest)
