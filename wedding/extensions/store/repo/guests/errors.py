"""Ошибки бд гостей."""
from wedding.extensions.store.global_errors import StoreError
from wedding.extensions.store.repo.guests.special_codes import (
    GUESTS_CONSTRAINT_ERROR,
    GUESTS_DB_ERROR,
    GUESTS_MULTIPLE_ROWS_FOUND_ERROR,
)

GUEST_MODEL_NAME = "GuestModel"


class GuestStoreError(StoreError):
    """Ошибка модели гостя."""

    special_code = GUESTS_DB_ERROR

    def __init__(self, msg: str):
        super().__init__(
            model=GUEST_MODEL_NAME,
            msg=msg,
        )


class GuestsConstraintError(GuestStoreError):
    """Конфликт данных гостей."""

    special_code = GUESTS_CONSTRAINT_ERROR

    def __init__(self, msg: str):
        super().__init__(msg=msg)


class MultipleGuestsFoundError(GuestStoreError):
    """Найдено несколько гостей, когда должен был найтись один."""

    special_code = GUESTS_MULTIPLE_ROWS_FOUND_ERROR

    def __init__(self, msg: str):
        super().__init__(msg=msg)
