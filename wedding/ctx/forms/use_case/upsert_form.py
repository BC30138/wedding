"""Сценария создания/обновления бланка ответов."""
import logging

from fastapi import Depends

from wedding.ctx.forms.dto.data import FormData, LoadFormsFiltersDTO
from wedding.ctx.forms.entity.structures import FormEntity
from wedding.ctx.forms.errors import FormNotFoundEntityError, FormValidationEntityError
from wedding.ctx.forms.service.forms_storage_service import FormsStorageService
from wedding.ctx.forms.special_codes import FORM_PLUS_ONE_FORBIDDEN
from wedding.ctx.groups.handler.get_group_handler import GetGroupHandler

logger = logging.getLogger().getChild("upsert_form_use_case")


class UpsertFormUseCase:
    """Сценария создания/обновления бланка ответов."""

    def __init__(
        self,
        forms_storage_service: FormsStorageService = Depends(FormsStorageService),
        group_service_api: GetGroupHandler = Depends(GetGroupHandler),
    ):
        self._forms_storage_service = forms_storage_service
        self._group_service_api = group_service_api

    async def execute(self, form_data: FormData, db_commit: bool) -> FormEntity:
        logger.info("Upserting form with data=%s", form_data)
        logger.info("Check group for form creation")
        group = await self._group_service_api.get_by_id_return_representation(
            group_id=form_data.group_id,
        )
        if group.is_couple and form_data.plus is not None:
            raise FormValidationEntityError(
                msg=f"Group {group.id} is couple, 'plus one' forbidden",
                special_code=FORM_PLUS_ONE_FORBIDDEN,
            )

        filters = LoadFormsFiltersDTO(group_ids=[form_data.group_id])
        form_entity = form_data.to_entity()

        try:
            logger.info("Find existing form with filters=%s", filters)
            existing_form_entity = await self._forms_storage_service.get_form_by(filters=filters)
            logger.info("Form update action")
            form_entity.id = existing_form_entity.id
        except FormNotFoundEntityError:
            logger.info("Form create action")

        return await self._forms_storage_service.create_form(
            entity=form_entity,
            db_commit=db_commit,
        )
