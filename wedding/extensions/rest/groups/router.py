"""API для работы с группами гостей"""
from http import HTTPStatus

from fastapi import APIRouter, Depends

from wedding.ctx.groups.errors import GroupNotFoundError
from wedding.ctx.groups.handler.create_group_handler import CreateGroupHandler
from wedding.ctx.groups.handler.get_group_handler import GetGroupHandler
from wedding.extensions.rest.groups.schema import GroupSchema, GroupDataSchema
from wedding.extensions.rest.helpers import ResponseGenerator

router = APIRouter(tags=["groups"])


@router.get(
    "/{group_id}",
    response_model=ResponseGenerator.success_schema(GroupSchema)
)
async def get_group(
    group_id: int,
    handler: GetGroupHandler = Depends(GetGroupHandler),
):
    try:
        group = await handler.get_by_id_return_schema(group_id=group_id)
        return ResponseGenerator.success(data=group)
    except GroupNotFoundError as exc:
        return ResponseGenerator.domain_error(
            exc=exc,
            status_code=HTTPStatus.NOT_FOUND,
        )


@router.post(
    "/",
    response_model=ResponseGenerator.success_schema(GroupSchema),
)
async def create_group(
    group_data: GroupDataSchema,
    handler: CreateGroupHandler = Depends(CreateGroupHandler),
):
    group = await handler.create_by_schema_return_schema(group_data_schema=group_data)
    return ResponseGenerator.success(data=group)
