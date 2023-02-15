from fastapi import Depends

from wedding.ctx.guests.dto.data import GuestData
from wedding.ctx.guests.dto.representations import GuestRepresentation
from wedding.ctx.guests.use_case.create_guest import CreateGuestUseCase
from wedding.extensions.rest.guests.schema import GuestDataSchema, GuestSchema


class CreateGuestHandler:
    def __init__(self, use_case: CreateGuestUseCase = Depends(CreateGuestUseCase)):
        self._use_case = use_case

    async def create_by_schema_return_schema(
        self,
        guest_data_schema: GuestDataSchema,
        db_commit: bool = True,
    ) -> GuestSchema:
        guest_data = guest_data_schema.to_dto()
        guest = await self._use_case.execute(
            guest_data=guest_data,
            db_commit=db_commit,
        )
        return GuestSchema.from_entity(entity=guest)

    async def create_by_dto_return_representation(
        self,
        guest_data: GuestData,
        db_commit: bool = False,
    ) -> GuestRepresentation:
        guest_entity = await self._use_case.execute(
            guest_data=guest_data,
            db_commit=db_commit,
        )
        return GuestRepresentation.from_entity(guest_entity=guest_entity)
