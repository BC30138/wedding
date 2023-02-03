"""API для работы с пользователями"""
from http import HTTPStatus

from fastapi import APIRouter, Depends

from wedding.ctx.groups.errors import GroupNotFoundError
from wedding.ctx.groups.handler.get_group_handler import GetGroupHandler
from wedding.extensions.rest.groups.schema import GroupSchema
from wedding.extensions.rest.helpers import ResponseGenerator

router = APIRouter(tags=["groups"])


@router.get(
    "/{group_id}",
    response_model=ResponseGenerator.success_schema(GroupSchema)
)
async def get_group(
    group_id: int,
    handler: GetGroupHandler = Depends(GetGroupHandler)
):
    try:
        group = await handler.get_by_id_return_schema(group_id=group_id)
        return ResponseGenerator.success(data=group)
    except GroupNotFoundError as exc:
        return ResponseGenerator.domain_error(
            exc=exc,
            status_code=HTTPStatus.NOT_FOUND,
        )
