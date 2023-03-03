"""Репозиторий для доступа к данным бланков ответов."""
import logging
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.exc import DBAPIError, IntegrityError, MultipleResultsFound
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select

from wedding.extensions.store.repo.base_repo import BaseRepo, RepoLoadFilters
from wedding.extensions.store.repo.forms.errors import FormsConstraintError, FormStoreError, MultipleFormsFoundError
from wedding.extensions.store.repo.forms.models import Forms

logger = logging.getLogger().getChild("forms_repo")


class LoadFormsFilters(RepoLoadFilters, total=False):
    group_ids: list[int] | None  # идентификаторы групп гостей


class FormsRepo(BaseRepo):
    """Репозиторий для доступа к данным бланков ответов."""

    def load_query(
        self,
        filters: LoadFormsFilters,
    ) -> Select:
        """
        Создает выборку для поиска бланков ответов

        :param filters: фильтры для поиска данных
        :return: выборка для поиска бланков ответов
        """
        logger.info("Building query for filters=%s", filters)
        query = select(Forms)
        if filters.get("group_ids", None) is not None:
            query = query.filter(Forms.group_id.in_(filters["group_ids"]))
        return query

    @contextmanager
    def _handle_load_one_errors(self, filters: LoadFormsFilters) -> Iterator[None]:
        """
        Контекст для того, чтобы ловить ошибки при загрузке одной записи.

        :raises MultipleFormsFoundError: когда найдено несколько записей
        """
        try:
            yield
        except MultipleResultsFound as exc:
            logger.warning("Multiple forms found for filters=%s", filters)
            raise MultipleFormsFoundError(msg=f"Multiple forms found for {filters=}") from exc

    @contextmanager
    def _handle_changes_errors(self) -> Iterator[None]:
        """
        Контекст для того, чтобы ловить ошибки при изменении/создании записи.

        :raises FormsConstraintError: когда произошел конфликт в бд
        :raises FormStoreError: нераспознанная ошибка бд
        """
        try:
            yield
        except IntegrityError as exc:
            logger.exception("Constraint error in Forms repo", exc_info=exc)
            raise FormsConstraintError(msg=str(exc)) from exc
        except DBAPIError as exc:
            logger.exception("Unexpected exception in Forms repo", exc_info=exc)
            raise FormStoreError(msg=str(exc)) from exc
