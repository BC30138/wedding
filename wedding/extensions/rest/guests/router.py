"""API для работы с гостями"""

from fastapi import APIRouter, Depends

from wedding.ctx.guests.handler.create_guest_handler import CreateGuestHandler
from wedding.ctx.guests.handler.get_guest_handler import GetGuestHandler
from wedding.extensions.rest.guests.schema import GuestSchema, GuestDataSchema
from wedding.extensions.rest.helpers import ResponseGenerator

router = APIRouter(tags=["guests"])


@router.get(
    "/{guest_id}",
    response_model=ResponseGenerator.success_schema(GuestSchema)
)
async def get_guest(
    guest_id: int,
    handler: GetGuestHandler = Depends(GetGuestHandler),
):
    guests = await handler.get_by_return_schema(guest_id=guest_id)
    return ResponseGenerator.success(data=guests)


@router.post(
    "/",
    response_model=ResponseGenerator.success_schema(GuestSchema),
)
async def create_guest(
    guest_data: GuestDataSchema,
    handler: CreateGuestHandler = Depends(CreateGuestHandler),
):
    guest = await handler.create_by_schema_return_schema(guest_data_schema=guest_data)
    return ResponseGenerator.success(data=guest)
