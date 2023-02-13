from fastapi import Request, Depends
from httpx import AsyncClient

from wedding.extensions.front.dto.back_dto import GroupInfo, GuestInfo
from wedding.extensions.front.helpers.rest_client import get_rest_client


class GroupService:
    def __init__(self, rest_client: AsyncClient = Depends(get_rest_client)):
        self._rest_client = rest_client
        self._base_path = "/private"

    def _build_path(self, url_path: str) -> str:
        return f"{self._base_path}{url_path}"

    async def get_group(self, group_id: int) -> GroupInfo:
        url_path = self._build_path(url_path=f"/groups/{group_id}")
        response = await self._rest_client.get(url_path)
        group_data = response.json()["data"]
        guest_1 = await self.get_guest(guest_id=group_data["guest_1_id"])
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
