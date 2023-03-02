"""Ошибки домена приглашений."""
from wedding.ctx.general_errors import DomainError
from wedding.ctx.invitations.special_codes import INV_GUEST_VALIDATION_ERROR

INV_GUEST_ENTITY_NAME = "INVITATION_GUEST"


class InvGuestEntityError(DomainError):
    """Ошибка связанная с сущностью гостя из приглашения."""

    def __init__(self, msg: str, special_code: str | None = None):
        super().__init__(entity=INV_GUEST_ENTITY_NAME, msg=msg, special_code=special_code)


class GuestValidationError(InvGuestEntityError):
    """Ошибка в данных гостя из приглашения"""

    special_code = INV_GUEST_VALIDATION_ERROR

    def __init__(self, msg: str, special_code: str | None = None):
        super().__init__(
            msg=msg,
            special_code=special_code,
        )
