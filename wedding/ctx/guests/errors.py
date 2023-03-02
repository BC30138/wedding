"""Ошибки домена guests."""
from wedding.ctx.general_errors import DomainError
from wedding.ctx.guests.special_codes import (
    GUEST_DOMAIN_ERROR,
    GUEST_MULTIPLE_FOUND,
    GUEST_NOT_FOUND,
    GUEST_VALIDATION_ERROR,
)

GUEST_ENTITY_NAME = "GuestEntity"


class GuestEntityError(DomainError):
    """Ошибка связанная с сущностью гостя."""

    special_code = GUEST_DOMAIN_ERROR

    def __init__(self, msg: str, special_code: str | None = None):
        super().__init__(
            entity=GUEST_ENTITY_NAME,
            msg=msg,
            special_code=special_code,
        )


class GuestNotFoundEntityError(GuestEntityError):
    """Гость не найден"""

    special_code = GUEST_NOT_FOUND

    def __init__(self, msg: str | None):
        msg = "Guest not found" if msg is None else msg
        super().__init__(msg=msg)


class GuestValidationEntityError(GuestEntityError):
    """Ошибка валидации гостя."""

    special_code = GUEST_VALIDATION_ERROR

    def __init__(self, msg: str | None, special_code: str | None):
        msg = "Guest validation error" if msg is None else msg
        super().__init__(
            msg=msg,
            special_code=special_code,
        )


class MultipleGuestsEntityError(GuestEntityError):
    """Несколько гостей найдено, когда ожидался один."""

    special_code = GUEST_MULTIPLE_FOUND

    def __init__(self, msg: str | None):
        msg = "Multiple guests found" if msg is None else msg
        super().__init__(msg=msg)
