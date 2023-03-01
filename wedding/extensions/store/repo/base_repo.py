"""Базовый репозиторий для взаимодействия с бд."""
import logging
from abc import abstractmethod
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, TypedDict

from fastapi import Depends
from sqlalchemy.exc import DBAPIError, IntegrityError, MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select

from wedding.extensions.store.database import Base, db_session
from wedding.extensions.store.global_errors import ConstraintError, MultipleRowsFoundError, StoreError

logger = logging.getLogger().getChild("base_repo")


UNDEFINED_MODEL_NAME = "UNDEFINED_MODEL_NAME"


class RepoLoadFilters(TypedDict):
    pass


class BaseRepo:
    """Базовый репозиторий для взаимодействия с бд."""

    def __init__(self, db_session: AsyncSession = Depends(db_session)):
        self._db_session = db_session

    @abstractmethod
    def load_query(self, filters: RepoLoadFilters) -> Select:  # noqa: U100
        """
        Выборка для получения данных из бд

        :param filters: фильтры для поиска
        """
        raise NotImplementedError

    @abstractmethod
    @contextmanager
    def _handle_changes_errors(self) -> Iterator[None]:
        """
        Контекст для того, чтобы ловить ошибки при изменении/создании записи.

        :raises ConstraintError: когда произошел конфликт в бд
        :raises StoreError: нераспознанная ошибка бд
        """
        try:
            yield
        except IntegrityError as exc:
            logger.exception(
                "Constraint error in repo %s",
                type(self).__name__,
                exc_info=exc,
            )
            raise ConstraintError(model=UNDEFINED_MODEL_NAME, msg=str(exc)) from exc
        except DBAPIError as exc:
            logger.exception(
                "Unexpected db error in repo %s",
                type(self).__name__,
                exc_info=exc,
            )
            raise StoreError(model=UNDEFINED_MODEL_NAME, msg=str(exc)) from exc

    @abstractmethod
    @contextmanager
    def _handle_load_one_errors(  # noqa: CCE001
        self,
        filters: RepoLoadFilters,
    ) -> Iterator[None]:
        """
        Контекст для того, чтобы ловить ошибки при загрузке одной записи.

        :param filters: фильтры для поиска

        :raises MultipleResultsFound: когда найдено несколько записей
        :raises StoreError: нераспознанная ошибка бд
        """
        try:
            yield
        except MultipleResultsFound as exc:
            logger.warning("Multiple results found for filters=%s", filters)
            raise MultipleRowsFoundError(
                model=UNDEFINED_MODEL_NAME,
                msg=f"Multiple results found for {filters=}",
            ) from exc
        except DBAPIError as exc:
            logger.exception(
                "Unexpected db error in repo %s with filters=%s",
                type(self).__name__,
                filters,
                exc_info=exc,
            )
            raise StoreError(model=UNDEFINED_MODEL_NAME, msg=str(exc)) from exc

    async def save(self, model: Base) -> Base:
        """
        Сохраняет/обновляет запись в бд

        :param model: модель, которую нужно сохранить/обновить
        :return: созданная/обновленная модель
        """
        logger.info("Saving model %s", model)
        with self._handle_changes_errors():
            model = await self._db_session.merge(model)
            await self._db_session.flush()
            await self._db_session.refresh(model)
            return model

    async def commit(self) -> None:
        """Коммитит изменения в бд."""
        logger.info("Commit changes in repo %s", type(self).__name__)
        with self._handle_changes_errors():
            await self._db_session.commit()

    async def load_one(self, filters: RepoLoadFilters) -> Any | None:
        """
        Ищет одну запись в бд.

        :param filters: фильтры для поиска
        """
        logger.info(
            "Loading one with filters=%s in repo %s",
            filters,
            type(self).__name__,
        )
        query = self.load_query(filters)
        with self._handle_load_one_errors(filters=filters):
            result = await self._db_session.execute(query)
            return result.scalar_one_or_none()
