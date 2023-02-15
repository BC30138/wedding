from fastapi import Depends

from wedding.ctx.groups.dto.data import GroupData
from wedding.ctx.groups.entity.group import GroupEntity
from wedding.ctx.groups.services.groups_service import GroupsService


class CreateGroupUseCase:
    def __init__(self, groups_service: GroupsService = Depends(GroupsService)):
        self._groups_service = groups_service

    async def execute(self, group_data: GroupData, db_commit: bool) -> GroupEntity:
        group = await self._groups_service.create_group(
            group_data=group_data,
            db_commit=db_commit
        )
        return group
