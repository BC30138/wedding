"""Сервис для доступа домена forms к хранилищу бланков ответов."""
import logging
from typing import cast

from fastapi import Depends

from wedding.ctx.forms.dto.data import LoadFormsFiltersDTO
from wedding.ctx.forms.entity.structures import FormEntity
from wedding.ctx.forms.errors import FormNotFoundEntityError, MultipleFormsEntityError
from wedding.extensions.store.repo.forms.errors import MultipleFormsFoundError
from wedding.extensions.store.repo.forms.models import Forms
from wedding.extensions.store.repo.forms.repo import FormsRepo, LoadFormsFilters

logger = logging.getLogger().getChild("forms_storage_service")


class FormsStorageService:
    """Сервис для доступа домена forms к хранилищу бланков ответов."""

    def __init__(self, forms_repo: FormsRepo = Depends(FormsRepo)):
        self._forms_repo = forms_repo

    async def get_form_by(
        self,
        filters: LoadFormsFiltersDTO,
    ) -> FormEntity:
        """
        Получения бланк из хранилища по идентификатору.

        :param filters: фильтры для поиска
        :return: сщуность бланка ответа

        :raises FormNotFoundError: когда бланк не найден
        :raises MultipleFormsEntityError: когда найдено несколько бланков
        """
        logger.info("Loading form with filters=%s", filters)
        db_filters = LoadFormsFilters(
            group_ids=filters.get("group_ids", None),
        )
        try:
            form_model = await self._forms_repo.load_one(
                filters=db_filters,
            )
        except MultipleFormsFoundError as exc:
            raise MultipleFormsEntityError(
                msg=f"By filters={filters} found multiple results",
            ) from exc
        form_model = cast(Forms, form_model)
        if form_model is None:
            logger.info("Form not found by filters=%s", filters)
            raise FormNotFoundEntityError(f"Form not found by {filters=}")
        return form_model.to_entity()

    async def create_form(self, entity: FormEntity, db_commit: bool) -> FormEntity:
        """
        Создает/обновляет бланк в бд

        :param entity: сущность бланка
        :param db_commit: нужно ли произвести коммит в хранилище
        :return: созданная сущность бланка
        """
        form_model = Forms.from_entity(entity=entity)
        form_model = await self._forms_repo.save(model=form_model)
        if db_commit:
            await self._forms_repo.commit()
        return form_model.to_entity()
