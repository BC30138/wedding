from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from wedding.extensions.front.helpers.mobility import mobility_manager, MobilityRequest, mobile_template_parser
from wedding.extensions.front.services.group_service import GroupService
from wedding.extensions.front.templates_storage import templates_storage

router = APIRouter(include_in_schema=False)


@router.get("/{group_id}", response_class=HTMLResponse)
@mobility_manager.is_mobile
async def get_invitation(
    request: MobilityRequest,
    group_id: int,
    group_service: GroupService = Depends(GroupService),
):
    template_name = mobile_template_parser(request=request, template_name="invitation.html")
    group = await group_service.get_group(group_id=group_id)
    return templates_storage.TemplateResponse(
        template_name,
        {
            "request": request,
            "group": group,
        }
    )