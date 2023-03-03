"""Хэндлер для сценария поиска одного бланка."""
from fastapi import Depends

from wedding.ctx.forms.dto.data import LoadFormsFiltersDTO
from wedding.ctx.forms.use_case.get_form import GetFormUseCase
from wedding.extensions.rest.forms.schema import FormSchema


class GetFormHandler:
    """Хэндлер для сценария поиска одного бланка."""

    def __init__(self, use_case: GetFormUseCase = Depends(GetFormUseCase)):
        self._use_case = use_case

    async def get_by_group_id_return_schema(self, group_id: int) -> FormSchema:
        """
        Получить бланк в виде pydantic схемы по идентификатору группы

        :param group_id: идентификатор группы
        :return: pydantic схема бланка
        """
        form_filters = LoadFormsFiltersDTO(group_ids=[group_id])
        guest = await self._use_case.execute(form_filters=form_filters)
        return FormSchema.from_entity(entity=guest)
