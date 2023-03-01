"""Репозиторий для доступа к данным гостей."""
import logging
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.exc import DBAPIError, IntegrityError, MultipleResultsFound
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select

from wedding.extensions.store.repo.base_repo import BaseRepo, RepoLoadFilters
from wedding.extensions.store.repo.guests.errors import GuestDBError, GuestsConstraintError, MultipleGuestsFoundError
from wedding.extensions.store.repo.guests.models import Guests

logger = logging.getLogger().getChild("guests_repo")


class LoadGuestsFilters(RepoLoadFilters, total=False):
    guest_ids: list[int] | None


class GuestsRepo(BaseRepo):
    """Репозиторий для доступа к данным гостей."""

    def load_query(
        self,
        filters: LoadGuestsFilters,
    ) -> Select:
        """
        Создает выборку для поиска гостей

        :param guest_ids: список идентификаторов гостей
        :return: выборка для поиска гостей
        """
        logger.info("Building query for filters=%s", filters)
        query = select(Guests)
        if filters.get("guest_ids", None) is not None:
            query = query.filter(Guests.id.in_(filters["guest_ids"]))
        return query

    @contextmanager
    def _handle_load_one_errors(self, filters: LoadGuestsFilters) -> Iterator[None]:
        """
        Контекст для того, чтобы ловить ошибки при загрузке одной записи.

        :raises MultipleGuestsFoundError: когда найдено несколько записей
        """
        try:
            yield
        except MultipleResultsFound as exc:
            logger.warning("Multiple guests found for filters=%s", filters)
            raise MultipleGuestsFoundError(msg=f"Multiple guests found for {filters=}") from exc

    @contextmanager
    def _handle_changes_errors(self) -> Iterator[None]:
        """
        Контекст для того, чтобы ловить ошибки при изменении/создании записи.

        :raises GuestsConstraintError: когда произошел конфликт в бд
        :raises GuestDBError: нераспознанная ошибка бд
        """
        try:
            yield
        except IntegrityError as exc:
            logger.exception("Constraint error in Guests repo", exc_info=exc)
            raise GuestsConstraintError(msg=str(exc)) from exc
        except DBAPIError as exc:
            logger.exception("Unexpected exception in Guests repo", exc_info=exc)
            raise GuestDBError(msg=str(exc)) from exc
