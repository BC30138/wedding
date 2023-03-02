"""Сервис для доступа домена guests к хранилищу гостей."""
import logging
from typing import Any, cast

from fastapi import Depends

from wedding.ctx.guests.dto.data import GuestData
from wedding.ctx.guests.entity.guest import GuestEntity
from wedding.ctx.guests.errors import GuestNotFoundEntityError, MultipleGuestsEntityError
from wedding.extensions.store.repo.guests.errors import MultipleGuestsFoundError
from wedding.extensions.store.repo.guests.models import Guests
from wedding.extensions.store.repo.guests.repo import GuestsRepo, LoadGuestsFilters

logger = logging.getLogger().getChild("storage_service")


class StorageService:
    """Сервис для доступа домена guests к хранилищу гостей."""

    def __init__(self, guests_repo: GuestsRepo = Depends(GuestsRepo)):
        self._guests_repo = guests_repo

    @staticmethod
    def create_guest_entity(guest_data: GuestData) -> GuestEntity:
        """
        Создать сущность гостя.

        :param guest_data: данные гостя
        :return: сущность гостя, пока что без id (не сохранена в хранилище)
        """
        logger.info("Creating entity from data %s", guest_data)
        return GuestEntity(
            first_name=guest_data.first_name,
            middle_name=guest_data.middle_name,
            last_name=guest_data.last_name,
            male=GuestEntity.cast_male(guest_data.male),
        )

    @staticmethod
    def guest_entity_to_model(entity: GuestEntity) -> Guests:
        """
        Преобразовывает сущность гостя в модель бд.

        :param entity: сущность гостя
        :return: модель гостя
        """
        logger.info("Creating model from entity %s", entity)
        kwagrs: dict[str, Any] = {
            "first_name": entity.first_name,
            "middle_name": entity.middle_name,
            "last_name": entity.last_name,
            "male": entity.male.value,
        }
        if entity.id:
            kwagrs["id"] = entity.id
        return Guests(**kwagrs)

    async def get_guest_by_id(
        self,
        guest_id: int,
    ) -> GuestEntity:
        """
        Получения гостя из хранилища по идентификатору.

        :param guest_id: идентификатор гостя
        :return: сщуность гостя

        :raises GuestNotFoundError: когда гость не найден
        """
        logger.info("Loading guest with id=%s", guest_id)
        try:
            guest_model = await self._guests_repo.load_one(
                filters=LoadGuestsFilters(guest_ids=[guest_id]),
            )
        except MultipleGuestsFoundError as exc:
            raise MultipleGuestsEntityError(
                msg=f"By id={guest_id} found multiple results",
            ) from exc
        guest_model = cast(Guests, guest_model)
        if guest_model is None:
            logger.info("Guest with id=%s not found", guest_id)
            raise GuestNotFoundEntityError(f"Guest with id {guest_id} not found")
        return guest_model.to_entity()

    async def create_guest(self, guest_data: GuestData, db_commit: bool) -> GuestEntity:
        """
        Создает гостя

        :param guest_data: данные о госте
        :param db_commit: нужно ли произвести коммит в хранилище
        :return: созданная сущность гостя
        """
        logger.info("Creating guest with data=%s", guest_data)
        guest_entity = self.create_guest_entity(guest_data=guest_data)
        guest_model = self.guest_entity_to_model(entity=guest_entity)
        guest_model = await self._guests_repo.save(model=guest_model)
        if db_commit:
            await self._guests_repo.commit()
        return guest_model.to_entity()
