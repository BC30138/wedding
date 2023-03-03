"""Хэндлер для обращения к сценарию обновления бланка ответов."""
from fastapi import Depends

from wedding.ctx.forms.use_case.upsert_form import UpsertFormUseCase
from wedding.extensions.rest.forms.schema import FormSchema, FormSchemaData


class UpsertFormHandler:
    def __init__(self, use_case: UpsertFormUseCase = Depends(UpsertFormUseCase)):
        self._use_case = use_case

    async def create_by_schema_return_schema(
        self,
        form_data_schema: FormSchemaData,
        db_commit: bool = True,
    ) -> FormSchemaData:
        """
        Создает/обновляет бланк по pydantic схеме.

        :param form_data_schema: pydantic с ответами
        :param db_commit: признак нужды сделать коммит
        :return: pydantic схема созданного бланка ответа
        """
        form_data = form_data_schema.to_dto()
        guest = await self._use_case.execute(
            form_data=form_data,
            db_commit=db_commit,
        )
        return FormSchema.from_entity(entity=guest)
