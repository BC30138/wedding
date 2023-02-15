from fastapi import Depends

from wedding.ctx.groups.dto.data import GroupData
from wedding.ctx.groups.dto.representations import GroupRepresentation
from wedding.ctx.groups.use_case.create_group import CreateGroupUseCase
from wedding.extensions.rest.groups.schema import GroupSchema, GroupDataSchema


class CreateGroupHandler:
    def __init__(self, use_case: CreateGroupUseCase = Depends(CreateGroupUseCase)):
        self._use_case = use_case

    async def create_by_schema_return_schema(
        self,
        group_data_schema: GroupDataSchema,
        db_commit: bool = True,
    ) -> GroupSchema:
        group_data = group_data_schema.to_dto()
        group = await self._use_case.execute(
            group_data=group_data,
            db_commit=db_commit,
        )
        return GroupSchema.from_entity(entity=group)

    async def create_by_dto_return_representation(
        self,
        group_data: GroupData,
        db_commit: bool = False,
    ) -> GroupRepresentation:
        group_entity = await self._use_case.execute(
            group_data=group_data,
            db_commit=db_commit,
        )
        return GroupRepresentation.from_entity(entity=group_entity)
