from http import HTTPStatus

from fastapi import APIRouter, Depends

from wedding.ctx.forms.errors import FormNotFoundEntityError
from wedding.ctx.forms.handler.get_form_handler import GetFormHandler
from wedding.extensions.rest.forms.schema import FormSchema
from wedding.extensions.rest.helpers import ResponseGenerator

router = APIRouter(tags=["private forms"])


@router.get(
    "/",
    response_model=ResponseGenerator.success_schema(FormSchema),
)
async def get_form_by(  # type: ignore
    group_id: int,
    upsert_form_handled: GetFormHandler = Depends(GetFormHandler),
):
    try:
        result = await upsert_form_handled.get_by_group_id_return_schema(
            group_id=group_id,
        )
    except FormNotFoundEntityError as exc:
        return ResponseGenerator.domain_error(exc=exc, status_code=HTTPStatus.NOT_FOUND)
    return ResponseGenerator.success(data=result)
