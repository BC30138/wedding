from fastapi import Depends

from wedding.ctx.guests.entity.guest import GuestEntity
from wedding.ctx.guests.service.storage_service import StorageService


class GetGuestUseCase:
    def __init__(self, storage_service: StorageService = Depends(StorageService)):
        self._storage_service = storage_service

    async def execute(self, guest_id: int) -> GuestEntity:
        return await self._storage_service.get_guest_by_id(guest_id=guest_id)
