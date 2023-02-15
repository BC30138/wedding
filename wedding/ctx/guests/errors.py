from wedding.ctx.general_errors import DomainError
from wedding.ctx.guests.entity.guest import GuestEntity
from wedding.ctx.guests.special_codes import GUEST_NOT_FOUND


class GuestNotFoundError(DomainError):
    def __init__(self, msg: str | None):
        msg = "Guest not found" if msg is None else msg
        super().__init__(
            entity=GuestEntity.__name__,
            msg=msg,
            special_code=GUEST_NOT_FOUND,
        )
