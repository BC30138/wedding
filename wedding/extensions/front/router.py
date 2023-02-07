from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from wedding.extensions.front.helpers.mobility import mobility_manager, MobilityRequest
from wedding.extensions.front.templates_storage import templates_storage

router = APIRouter(include_in_schema=False)


@router.get("/{group_id}", response_class=HTMLResponse)
@mobility_manager.is_mobile
async def get_invitation(request: MobilityRequest, group_id: int):
    return templates_storage.TemplateResponse("invitation.html", {"request": request})
