from fastapi import Depends

from wedding.ctx.groups.dto.data import GroupData as DomainGroupData
from wedding.ctx.groups.dto.representations import GroupRepresentation
from wedding.ctx.groups.handler.create_group_handler import CreateGroupHandler
from wedding.ctx.groups.handler.get_group_batch_handler import GetGroupBatchHandler
from wedding.ctx.invitations.dto.data import GroupData
from wedding.ctx.invitations.entity.structures import GroupEntity


class GroupsService:
    def __init__(
        self,
        create_group_api: CreateGroupHandler = Depends(CreateGroupHandler),
        get_group_batch_api: GetGroupBatchHandler = Depends(GetGroupBatchHandler),
    ):
        self._create_group_api = create_group_api
        self._get_group_batch_api = get_group_batch_api

    @staticmethod
    def create_entity_from_representation(
        representation: GroupRepresentation,
    ) -> GroupEntity:
        return GroupEntity(
            id=representation.id,
            name=representation.name,
            guest_1_id=representation.guest_1_id,
            guest_2_id=representation.guest_2_id,
            is_couple=representation.is_couple,
            form_id=representation.form_id,
        )

    async def create_group(
        self,
        group_data: GroupData,
        guest_1_id: int,
        guest_2_id: int | None,
    ) -> GroupEntity:
        group_data = DomainGroupData(
            name=group_data.name,
            guest_1_id=guest_1_id,
            guest_2_id=guest_2_id,
        )
        group_repr = await self._create_group_api.create_by_dto_return_representation(
            group_data=group_data,
            db_commit=False,
        )
        return self.create_entity_from_representation(
            representation=group_repr,
        )

    async def get_all_groups(self) -> list[GroupEntity]:
        groups_representations = await self._get_group_batch_api.get_all_return_representations()
        return [
            self.create_entity_from_representation(
                representation=group_representation,
            ) for group_representation in groups_representations
        ]
