from wedding.ctx.general_errors import DomainError
from wedding.ctx.groups.entity.group import GroupEntity
from wedding.ctx.groups.special_codes import GROUP_NOT_FOUND


class GroupNotFoundError(DomainError):
    def __init__(self, msg: str | None):
        msg = "Group not found" if msg is None else msg
        super().__init__(
            entity=GroupEntity.__name__,
            msg=msg,
            special_code=GROUP_NOT_FOUND,
        )
