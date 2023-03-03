from fastapi import APIRouter, Depends

from wedding.ctx.forms.handler.upsert_form_handler import UpsertFormHandler
from wedding.extensions.rest.forms.schema import FormSchema, FormSchemaData
from wedding.extensions.rest.helpers import ResponseGenerator

router = APIRouter(tags=["forms"])


@router.put(
    "/",
    response_model=ResponseGenerator.success_schema(FormSchema),
)
async def upsert_form_answer(  # type: ignore
    form_data: FormSchemaData,
    upsert_form_handled: UpsertFormHandler = Depends(UpsertFormHandler),
):
    result = await upsert_form_handled.create_by_schema_return_schema(
        form_data_schema=form_data,
    )
    return ResponseGenerator.success(data=result)
