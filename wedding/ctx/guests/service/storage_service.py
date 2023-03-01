from typing import Any, cast

from fastapi import Depends

from wedding.ctx.guests.dto.data import GuestData
from wedding.ctx.guests.entity.guest import GuestEntity, MaleEnum
from wedding.ctx.guests.errors import GuestNotFoundError
from wedding.extensions.store.repo.guests.models import Guests
from wedding.extensions.store.repo.guests.repo import GuestsRepo, LoadGuestsFilters


class StorageService:
    def __init__(self, guests_repo: GuestsRepo = Depends(GuestsRepo)):
        self._guests_repo = guests_repo

    @staticmethod
    def create_guest_entity(guest_data: GuestData) -> GuestEntity:
        return GuestEntity(
            first_name=guest_data.first_name,
            middle_name=guest_data.middle_name,
            last_name=guest_data.last_name,
            male=MaleEnum(guest_data.male),
        )

    @staticmethod
    def guest_entity_to_model(entity: GuestEntity) -> Guests:
        kwagrs: dict[str, Any] = {
            "first_name": entity.first_name,
            "middle_name": entity.middle_name,
            "last_name": entity.last_name,
            "male": entity.male.value,
        }
        if entity.id:
            kwagrs["id"] = entity.id
        return Guests(**kwagrs)

    async def get_guest_by_id(
        self,
        guest_id: int,
    ) -> GuestEntity:
        guest_model = await self._guests_repo.load_one(
            filters=LoadGuestsFilters(guest_ids=[guest_id]),
        )
        guest_model = cast(Guests, guest_model)
        if guest_model is None:
            raise GuestNotFoundError(f"Guest with id {guest_id} not found")
        return guest_model.to_entity()

    async def create_guest(self, guest_data: GuestData, db_commit: bool) -> GuestEntity:
        guest_entity = self.create_guest_entity(guest_data=guest_data)
        guest_model = self.guest_entity_to_model(entity=guest_entity)
        guest_model = await self._guests_repo.save(model=guest_model)
        if db_commit:
            await self._guests_repo.commit()
        return guest_model.to_entity()
