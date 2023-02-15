from fastapi import Depends

from wedding.ctx.guests.dto.data import GuestData
from wedding.ctx.guests.entity.guest import GuestEntity
from wedding.ctx.guests.service.storage_service import StorageService


class CreateGuestUseCase:
    def __init__(self, storage_service: StorageService = Depends(StorageService)):
        self._storage_service = storage_service

    async def execute(self, guest_data: GuestData, db_commit: bool) -> GuestEntity:
        guest = await self._storage_service.create_guest(
            guest_data=guest_data,
            db_commit=db_commit,
        )
        return guest
