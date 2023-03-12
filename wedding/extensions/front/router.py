from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from wedding.cfg import app_configuration
from wedding.extensions.front.helpers.mobility import MobilityRequest, mobile_template_parser, mobility_manager
from wedding.extensions.front.services.group_service import GroupService
from wedding.extensions.front.templates_storage import templates_storage

router = APIRouter(include_in_schema=False)


@router.get("/{group_id}", response_class=HTMLResponse)
@mobility_manager.is_mobile_decorator
async def get_invitation(  # type: ignore
    request: MobilityRequest,
    group_id: int,
    update_form: bool = False,
    group_service: GroupService = Depends(GroupService),
):
    template_name = mobile_template_parser(request=request, template_name="invitation.html")
    group = await group_service.get_group(group_id=group_id)
    return templates_storage.TemplateResponse(
        template_name,
        {
            "request": request,
            "group": group,
            "update_form": update_form,
            "static_url": app_configuration.static_cdn,
        },
    )
