from wedding.ctx.general_errors import EntityValidationError
from wedding.ctx.invitations.entity.structures import GuestEntity


class GuestValidationError(EntityValidationError):
    def __init__(self, msg: str, special_code: str | None = None):
        self.entity = GuestEntity.__name__
        self.msg = msg
        self.special_code = special_code
        super().__init__(self.entity, self.msg, self.special_code)
