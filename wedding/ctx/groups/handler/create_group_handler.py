from fastapi import Depends

from wedding.ctx.groups.use_case.create_group import CreateGroupUseCase
from wedding.extensions.rest.groups.schema import GroupSchema, GroupDataSchema


class CreateGroupHandler:
    def __init__(self, use_case: CreateGroupUseCase = Depends(CreateGroupUseCase)):
        self._use_case = use_case

    async def create_by_schema_return_schema(self, group_data_schema: GroupDataSchema) -> GroupSchema:
        group_data = group_data_schema.to_dto()
        group = await self._use_case.execute(group_data=group_data)
        return GroupSchema.from_entity(entity=group)
