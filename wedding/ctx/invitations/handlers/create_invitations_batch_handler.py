import csv
from io import StringIO

from fastapi import Depends

from wedding.ctx.invitations.use_case.create_invitations_batch import CreateInvitationsBatchUseCase
from wedding.extensions.rest.invitations.schema import InvitationSchema


class CreateInvitationsBatchHandler:
    def __init__(self, use_case: CreateInvitationsBatchUseCase = Depends(CreateInvitationsBatchUseCase)):
        self._use_case = use_case

    def create_from_csv_return_schema(self, csv_file_bytes: bytes) -> list[InvitationSchema]:
        content = csv_file_bytes.decode()
        file = StringIO(content)
        csv_data = csv.reader(file, delimiter=",")
        print(csv_data)
