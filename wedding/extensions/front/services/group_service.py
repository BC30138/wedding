from fastapi import Depends
from httpx import AsyncClient

from wedding.extensions.front.dto.back_dto import GroupInfo, GuestInfo
from wedding.extensions.front.helpers.rest_client import get_rest_client
from wedding.extensions.front.services.errors import GuestNotProvided
from wedding.extensions.front.services.special_codes import GUEST_1_NOT_PROVIDED


class GroupService:
    def __init__(self, rest_client: AsyncClient = Depends(get_rest_client)):
        self._rest_client = rest_client
        self._base_path = "/private"

    async def get_group(self, group_id: int) -> GroupInfo:
        url_path = self._build_path(url_path=f"/groups/{group_id}")
        response = await self._rest_client.get(url_path)
        group_data = response.json()["data"]
        guest_1 = await self.get_guest(guest_id=group_data["guest_1_id"])
        if guest_1 is None:
            raise GuestNotProvided(
                service=GroupService.__name__,
                msg=f"Guest 1 must be provided, {group_id=}",
                special_code=GUEST_1_NOT_PROVIDED,
            )

        guest_2 = await self.get_guest(guest_id=group_data["guest_2_id"])
        return GroupInfo.from_json(
            json_data=group_data,
            guest_1=guest_1,
            guest_2=guest_2,
        )

    async def get_guest(self, guest_id: int | None) -> GuestInfo | None:
        if guest_id is None:
            return None
        url_path = self._build_path(url_path=f"/guests/{guest_id}")
        response = await self._rest_client.get(url_path)
        guest_data = response.json()["data"]
        return GuestInfo.from_json(json_data=guest_data)

    def _build_path(self, url_path: str) -> str:
        return f"{self._base_path}{url_path}"
