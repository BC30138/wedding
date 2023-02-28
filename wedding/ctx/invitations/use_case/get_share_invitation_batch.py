from fastapi import Depends

from wedding.ctx.invitations.entity.structures import ShareInvitationEntity
from wedding.ctx.invitations.services.groups_service import GroupsService
from wedding.ctx.invitations.services.guests_service import GuestsService


class GetShareInvitationBatchUseCase:
    def __init__(
        self,
        groups_service: GroupsService = Depends(GroupsService),
        guests_service: GuestsService = Depends(GuestsService),
    ):
        self._groups_service = groups_service
        self._guests_service = guests_service

    async def execute(self, base_url: str) -> list[ShareInvitationEntity]:
        invitations = []
        groups = await self._groups_service.get_all_groups()
        for group in groups:
            guest_1 = await self._guests_service.get_guest(guest_id=group.guest_1_id)
            guest_2 = (
                await self._guests_service.get_guest(
                    guest_id=group.guest_2_id,
                )
                if group.guest_2_id is not None
                else None
            )
            invitations.append(
                ShareInvitationEntity.from_entities(
                    group=group,
                    guest_1=guest_1,
                    guest_2=guest_2,
                    base_url=base_url,
                ),
            )
        return invitations
