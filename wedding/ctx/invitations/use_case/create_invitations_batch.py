from fastapi import Depends

from wedding.ctx.invitations.dto.data import InvitationDataDTO
from wedding.ctx.invitations.entity.structures import InvitationEntity
from wedding.ctx.invitations.services.groups_service import GroupsService
from wedding.ctx.invitations.services.guests_service import GuestsService
from wedding.ctx.invitations.services.storage_service import StorageService


class CreateInvitationsBatchUseCase:
    def __init__(
        self,
        guests_service: GuestsService = Depends(GuestsService),
        groups_service: GroupsService = Depends(GroupsService),
        storage_service: StorageService = Depends(StorageService),
    ):
        self._guests_service = guests_service
        self._groups_service = groups_service
        self._storage_service = storage_service

    async def execute(
        self,
        invitation_data_batch: list[InvitationDataDTO],
        db_commit: bool,
    ) -> list[InvitationEntity]:
        result = []
        for invitation_data in invitation_data_batch:
            guest_1 = await self._guests_service.create_guest(
                guest_data=invitation_data.guest_1,
            )
            guest_2 = (
                await self._guests_service.create_guest(
                    guest_data=invitation_data.guest_2,
                )
                if invitation_data.guest_2 is not None
                else None
            )
            group = await self._groups_service.create_group(
                group_data=invitation_data.group,
                guest_1_id=guest_1.id,
                guest_2_id=guest_2.id if guest_2 else None,
            )
            result.append(
                InvitationEntity(group=group, guest_1=guest_1, guest_2=guest_2),
            )

        if db_commit:
            await self._storage_service.commit()
        return result
