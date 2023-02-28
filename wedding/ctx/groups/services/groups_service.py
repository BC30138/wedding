from fastapi import Depends

from wedding.ctx.groups.dto.data import GroupData
from wedding.ctx.groups.entity.group import GroupEntity
from wedding.ctx.groups.errors import GroupNotFoundError
from wedding.extensions.store.repo.groups.models import Groups
from wedding.extensions.store.repo.groups.repo import GroupsRepo


class GroupsService:
    def __init__(self, groups_repo: GroupsRepo = Depends(GroupsRepo)):
        self._groups_repo = groups_repo

    @staticmethod
    def create_group_entity(group_data: GroupData) -> GroupEntity:
        return GroupEntity(
            name=group_data.name,
            guest_1_id=group_data.guest_1_id,
            guest_2_id=group_data.guest_2_id,
        )

    @staticmethod
    def group_entity_to_model(entity: GroupEntity) -> Groups:
        return Groups(
            name=entity.name,
            guest_1_id=entity.guest_1_id,
            guest_2_id=entity.guest_2_id,
        )

    async def get_group_by(
        self,
        group_id: int | None = None,
        name: str | None = None,
    ) -> GroupEntity:
        group_model = await self._groups_repo.load_one(
            group_id=group_id,
            name=name,
        )
        if group_model is None:
            raise GroupNotFoundError(f"Group with id {group_id} not found")
        return group_model.to_entity()

    async def get_group_batch_by(self) -> list[GroupEntity]:
        group_models = await self._groups_repo.load_all()
        return [group_model.to_entity() for group_model in group_models]

    async def create_group(self, group_data: GroupData, db_commit: bool) -> GroupEntity:
        group_entity = self.create_group_entity(group_data=group_data)
        group_model = self.group_entity_to_model(entity=group_entity)
        group_model = await self._groups_repo.save(group=group_model)
        if db_commit:
            await self._groups_repo.commit()
        return group_model.to_entity()
