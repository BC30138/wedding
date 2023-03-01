"""Ошибки домена guests."""
from wedding.ctx.general_errors import DomainError, EntityValidationError
from wedding.ctx.guests.special_codes import GUEST_NOT_FOUND, GUEST_VALIDATION_ERROR

GUEST_ENTITY_NAME = "GuestEntity"


class GuestNotFoundError(DomainError):
    """Гость не найден"""

    def __init__(self, msg: str | None):
        msg = "Guest not found" if msg is None else msg
        super().__init__(
            entity=GUEST_ENTITY_NAME,
            msg=msg,
            special_code=GUEST_NOT_FOUND,
        )


class GuestEntityValidationError(EntityValidationError):
    """Ошибка валидации гостя."""

    special_code = GUEST_VALIDATION_ERROR

    def __init__(self, msg: str | None, special_code: str | None = None):
        msg = "Guest validation error" if msg is None else msg
        super().__init__(
            entity=GUEST_ENTITY_NAME,
            msg=msg,
            special_code=special_code,
        )
