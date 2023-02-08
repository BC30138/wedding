from fastapi import Depends

from wedding.ctx import GuestNotFoundError
from wedding.ctx.guests.dto.data import GuestData
from wedding.ctx.guests.entity.guest import GuestEntity, MaleEnum
from wedding.extensions.store.repo.guests.models import Guests
from wedding.extensions.store.repo.guests.repo import GuestsRepo


class StorageService:
    def __init__(self, guests_repo: GuestsRepo = Depends(GuestsRepo)):
        self._guests_repo = guests_repo

    @staticmethod
    def create_guest_entity(guest_data: GuestData) -> GuestEntity:
        return GuestEntity(
            first_name=guest_data.first_name,
            middle_name=guest_data.middle_name,
            last_name=guest_data.last_name,
            group_id=guest_data.group_id,
            male=MaleEnum(guest_data.male),
        )

    @staticmethod
    def guest_entity_to_model(entity: GuestEntity) -> Guests:
        return Guests(
            first_name=entity.first_name,
            middle_name=entity.middle_name,
            last_name=entity.last_name,
            group_id=entity.group_id,
            male=entity.male.value,
        )

    async def get_guest_list_by(
        self,
        group_id: int | None = None,
    ) -> list[GuestEntity]:
        guest_models = await self._guests_repo.load(
            group_id=group_id,
        )
        return [guest_model.to_entity() for guest_model in guest_models]

    async def get_guest_by_id(
        self,
        guest_id: int,
    ) -> GuestEntity:
        guest_model = await self._guests_repo.load_one(guest_id=guest_id)
        if guest_model is None:
            raise GuestNotFoundError(f"Guest with id {guest_id} not found")
        return guest_model.to_entity()

    async def create_guest(self, guest_data: GuestData):
        guest_entity = self.create_guest_entity(guest_data=guest_data)
        guest_model = self.guest_entity_to_model(entity=guest_entity)
        guest_model = await self._guests_repo.save(guest=guest_model)
        return guest_model.to_entity()
