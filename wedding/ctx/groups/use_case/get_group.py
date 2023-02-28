from fastapi import Depends

from wedding.ctx.groups.entity.group import GroupEntity
from wedding.ctx.groups.services.groups_service import GroupsService


class GetGroupUseCase:
    def __init__(self, groups_service: GroupsService = Depends(GroupsService)):
        self._groups_service = groups_service

    async def execute(self, group_id: int) -> GroupEntity:
        return await self._groups_service.get_group_by(group_id=group_id)
