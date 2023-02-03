from fastapi import Depends

from wedding.ctx.groups.entity.group import GroupEntity
from wedding.ctx.groups.errors import GroupNotFoundError
from wedding.extensions.store.repo.groups.repo import GroupsRepo


class GroupsService:
    def __init__(self, groups_repo: GroupsRepo = Depends(GroupsRepo)):
        self._groups_repo = groups_repo

    async def get_group_by_id(
        self,
        group_id: int,
    ) -> GroupEntity:
        group_model = await self._groups_repo.get_by_id(group_id=group_id)
        if group_model is None:
            raise GroupNotFoundError(f"Group with id {group_id} not found")
        return group_model.to_entity()

