from fastapi import Depends

from wedding.ctx.guests.use_case.get_guest_list import GetGuestListUseCase
from wedding.extensions.rest.guests.schema import GuestSchema


class GetGuestListHandler:
    def __init__(self, use_case: GetGuestListUseCase = Depends(GetGuestListUseCase)):
        self._use_case = use_case

    async def get_list_by_return_schema(self, group_id: int) -> list[GuestSchema]:
        guest_list = await self._use_case.execute(group_id=group_id)
        return [GuestSchema.from_entity(entity=guest) for guest in guest_list]
