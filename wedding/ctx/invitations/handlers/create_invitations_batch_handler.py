from io import StringIO
from typing import TypedDict

from fastapi import Depends
from aiocsv import AsyncDictReader
from apyio import StringIO

from wedding.ctx.invitations.dto.data import InvitationDataDTO, GroupData, GuestData
from wedding.ctx.invitations.errors import GuestValidationError
from wedding.ctx.invitations.special_codes import GUEST_NAME_VALIDATION_ERROR, GUEST_MALE_VALIDATION_ERROR
from wedding.ctx.invitations.use_case.create_invitations_batch import CreateInvitationsBatchUseCase
from wedding.extensions.rest.invitations.schema import InvitationSchema


class CsvRowDict(TypedDict):
    name: str
    guest_1: str
    male_1: str
    guest_2: str
    male_2: str


class CreateInvitationsBatchHandler:
    def __init__(self, use_case: CreateInvitationsBatchUseCase = Depends(CreateInvitationsBatchUseCase)):
        self._use_case = use_case

    def create_guest_data(self, string_name: str, male: str) -> GuestData:
        if male == 'f' or male == 'female':
            male = 'female'
        elif male == 'm' or male == 'male':
            male = 'male'
        else:
            GuestValidationError(
                msg=f"Wrong male: {male}",
                special_code=GUEST_MALE_VALIDATION_ERROR,
            )

        split_name_data = string_name.strip()
        split_name_data = split_name_data.split(" ")
        if len(split_name_data) == 2:
            first_name = split_name_data[1]
            last_name = split_name_data[0]
            middle_name = None
        elif len(split_name_data) == 3:
            first_name = split_name_data[1]
            last_name = split_name_data[0]
            middle_name = split_name_data[2]
        else:
            raise GuestValidationError(
                msg=f"Incorrect full name format: {string_name}",
                special_code=GUEST_NAME_VALIDATION_ERROR,
            )

        return GuestData(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            male=male,
        )


    def csv_row_to_data_dto(self, csv_row: CsvRowDict) -> InvitationDataDTO:
        return InvitationDataDTO(
            group=GroupData(
                name=csv_row['name'],
            ),
            guest_1=self.create_guest_data(
                string_name=csv_row['guest_1'],
                male=csv_row['male_1'],
            ),
            guest_2=self.create_guest_data(
                string_name=csv_row['guest_2'],
                male=csv_row['male_2'],
            ) if csv_row.get('guest_2') else None,
        )

    async def create_from_csv_return_schema(self, csv_file_bytes: bytes) -> list[InvitationSchema]:
        content = csv_file_bytes.decode()
        file = StringIO(content)

        invitation_data_batch = []
        async for row in AsyncDictReader(file):
            invitation_data_batch.append(self.csv_row_to_data_dto(csv_row=row))

        result = await self._use_case.execute(
            invitation_data_batch=invitation_data_batch,
            db_commit=True,
        )
        return [InvitationSchema.from_entity(entity=entity) for entity in result]
