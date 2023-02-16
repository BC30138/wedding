from fastapi import Depends

from wedding.ctx.groups.dto.representations import GroupRepresentation
from wedding.ctx.groups.use_case.get_group_batch import GetGroupBatchUseCase


class GetGroupBatchHandler:
    def __init__(self, use_case: GetGroupBatchUseCase = Depends(GetGroupBatchUseCase)):
        self._use_case = use_case

    async def get_all_return_representations(self) -> list[GroupRepresentation]:
        groups = await self._use_case.execute()
        return [GroupRepresentation.from_entity(entity=group) for group in groups]
