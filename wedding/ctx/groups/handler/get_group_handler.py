from fastapi import Depends

from wedding.ctx.groups.use_case.get_group import GetGroupUseCase
from wedding.extensions.rest.groups.schema import GroupSchema


class GetGroupHandler:
    def __init__(self, use_case: GetGroupUseCase = Depends(GetGroupUseCase)):
        self._use_case = use_case

    async def get_by_id_return_schema(self, group_id: int) -> GroupSchema:
        group = await self._use_case.execute(group_id=group_id)
        return GroupSchema.from_entity(entity=group)
