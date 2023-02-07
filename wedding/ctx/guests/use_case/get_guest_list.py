from fastapi import Depends

from wedding.ctx.guests.entity.guest import GuestEntity
from wedding.ctx.guests.service.storage_service import StorageService


class GetGuestListUseCase:
    def __init__(self, storage_service: StorageService = Depends(StorageService)):
        self._storage_service = storage_service

    async def execute(self, group_id: int) -> list[GuestEntity]:
        guests = await self._storage_service.get_guest_list_by(group_id=group_id)
        return guests
