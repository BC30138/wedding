"""API для работы с гостями"""
from http import HTTPStatus

from fastapi import APIRouter, Depends

from wedding.ctx.groups.errors import GroupNotFoundError
from wedding.ctx.groups.handler.create_group_handler import CreateGroupHandler
from wedding.ctx.groups.handler.get_group_handler import GetGroupHandler
from wedding.ctx.guests.handler.create_guest_handler import CreateGuestHandler
from wedding.ctx.guests.handler.get_guest_list_handler import GetGuestListHandler
from wedding.extensions.rest.groups.schema import GroupSchema, GroupDataSchema
from wedding.extensions.rest.guests.schema import GuestSchema, GuestDataSchema
from wedding.extensions.rest.helpers import ResponseGenerator

router = APIRouter(tags=["guests"])


@router.get(
    "/",
    response_model=ResponseGenerator.success_schema(list[GuestSchema])
)
async def get_guests(
    group_id: int,
    handler: GetGuestListHandler = Depends(GetGuestListHandler),
):
    guests = await handler.get_list_by_return_schema(group_id=group_id)
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
