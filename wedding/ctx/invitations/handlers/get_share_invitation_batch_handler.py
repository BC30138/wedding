import csv
from typing import TypedDict, cast

from aiocsv import AsyncDictWriter
from fastapi import Depends

from wedding.ctx.invitations.entity.structures import ShareInvitationEntity
from wedding.ctx.invitations.use_case.get_share_invitation_batch import GetShareInvitationBatchUseCase
from wedding.helpers.apyio_extender import StringIO


class CsvRowDict(TypedDict):
    num: int
    name: str
    guest_1: str
    guest_2: str | None
    link: str


class GetShareInvitationBatchHandler:
    def __init__(self, use_case: GetShareInvitationBatchUseCase = Depends(GetShareInvitationBatchUseCase)):
        self._use_case = use_case

    @staticmethod
    def entity_to_csv_row(num: int, entity: ShareInvitationEntity) -> CsvRowDict:
        return CsvRowDict(
            num=num,
            name=entity.group_name,
            guest_1=entity.guest_1_full_name,
            guest_2=entity.guest_2_full_name,
            link=entity.link,
        )

    async def get_all_return_csv(self, base_url: str) -> bytes:
        result = await self._use_case.execute(base_url=base_url)

        file = StringIO()
        writer = AsyncDictWriter(file, CsvRowDict.__annotations__.keys(), restval="", quoting=csv.QUOTE_ALL)
        await writer.writeheader()

        for it, invitation in enumerate(result):
            row = self.entity_to_csv_row(num=it + 1, entity=invitation)
            await writer.writerow(row)

        bytes_result = file.getvalue().encode()
        return cast(bytes, bytes_result)
