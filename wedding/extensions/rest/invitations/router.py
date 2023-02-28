from fastapi import APIRouter, Depends, File, Request

from wedding.ctx.invitations.handlers.create_invitations_batch_handler import CreateInvitationsBatchHandler
from wedding.ctx.invitations.handlers.get_share_invitation_batch_handler import GetShareInvitationBatchHandler
from wedding.extensions.rest.helpers import CsvResponse, ResponseGenerator
from wedding.extensions.rest.invitations.schema import InvitationSchema

router = APIRouter(tags=["invitations"])


@router.post(
    "/import/csv",
    response_model=ResponseGenerator.success_schema(
        list[InvitationSchema],
    ),
)
async def upload_invitations(  # type: ignore
    file: bytes = File(),
    handler: CreateInvitationsBatchHandler = Depends(CreateInvitationsBatchHandler),
):
    result = await handler.create_from_csv_return_schema(csv_file_bytes=file)
    return ResponseGenerator.success(data=result)


@router.get(
    "/export/csv",
    response_class=CsvResponse,
)
async def download_invitations(  # type: ignore
    request: Request,
    handler: GetShareInvitationBatchHandler = Depends(GetShareInvitationBatchHandler),
):
    result = await handler.get_all_return_csv(base_url=str(request.base_url))
    return CsvResponse.success(content=result)
