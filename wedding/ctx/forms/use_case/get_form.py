"""Сценарий поиска одного бланка."""
from fastapi import Depends

from wedding.ctx.forms.dto.data import LoadFormsFiltersDTO
from wedding.ctx.forms.entity.structures import FormEntity
from wedding.ctx.forms.service.forms_storage_service import FormsStorageService


class GetFormUseCase:
    """Сценарий поиска одного бланка."""

    def __init__(self, forms_storage_service: FormsStorageService = Depends(FormsStorageService)):
        self._forms_storage_service = forms_storage_service

    async def execute(self, form_filters: LoadFormsFiltersDTO) -> FormEntity:
        return await self._forms_storage_service.get_form_by(filters=form_filters)
