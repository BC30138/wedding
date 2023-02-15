from fastapi import APIRouter, File, Depends

from wedding.ctx.invitations.handlers.create_invitations_batch_handler import CreateInvitationsBatchHandler
from wedding.extensions.rest.helpers import ResponseGenerator
from wedding.extensions.rest.invitations.schema import InvitationSchema

router = APIRouter(tags=["invitations"])


@router.post(
    "/",
    response_model=ResponseGenerator.success_schema(
        list[InvitationSchema],
    )
)
async def upload_invitations(
    file: bytes = File(),
    handler: CreateInvitationsBatchHandler = Depends(CreateInvitationsBatchHandler),
):
    result = await handler.create_from_csv_return_schema(csv_file_bytes=file)
    return ResponseGenerator.success(data=result)
